Title: Cloning a running Windows PC to a KVM virtual machine image
Date: 2026-05-02 20:00
Category: Cool Tricks
Tags: windows, kvm, sysinternals, disk2vhd
Slug: disk2vhd-kvm
Authors: Difegue
HeroImage: images/crt-wsl2.jpg
Summary: 

If you have a running Windows PC you want to virtualize due to aging/dying hardware, a good solution is to migrate it to your homelab that's probably running Linux.  
I had to do this recently for a W11 machine, and while none of the steps here are new, I thought it'd be worthwhile to collate all the information in one spot.  

# Use Disk2vhd to snapshot the install  

[Disk2vhd](https://learn.microsoft.com/en-us/sysinternals/downloads/disk2vhd) is an interesting tool to use here as it allows you to snapshot the disk to VHD while Windows is still running, instead of having to turn the machine off and dump the disk.    

> The difference between Disk2vhd and other physical-to-virtual tools is that you can run Disk2vhd on a system that’s online. Disk2vhd uses Windows' Volume Snapshot capability, introduced in Windows XP, to create consistent point-in-time snapshots of the volumes you want to include in a conversion.  

![Disk2vhd screenshot](https://learn.microsoft.com/en-us/sysinternals/downloads/media/disk2vhd/20131218_disk2vhd_v2.0.png)  

The snapshot will take a long time depending on disk size, but this works just fine. I did check the "_Use Vhdx_" box as snapshotting wouldn't work otherwise.  

You _might_ want to install the [KVM drivers](https://virtio-win.github.io/Knowledge-Base/Driver-installation.html) to the physical Windows machine before snapshotting it, as otherwise you'll have to sideload these later on.  

# Convert the VHDX image to QCow2  

Once you have your VHDX, you can convert it to a KVM-sanctioned format on a Linux machine:  
```
qemu-img convert -O qcow2 Windows.vhdx Windows.qcow2
```  

This will take a similarly long time depending on disk size. You can verify the basic size of the image afterwards:  
```
qemu-img info Windows.qcow2  

image: Windows.qcow2
file format: qcow2
virtual size: 1.86 TiB (2048408248320 bytes)
disk size: 728 GiB
cluster_size: 65536
Format specific information:
    compat: 1.1
    compression type: zlib
    lazy refcounts: false
    refcount bits: 16
    corrupt: false
    extended l2: false
Child node '/file':
    filename: Windows.qcow2
    protocol type: file
    file length: 728 GiB (782145486848 bytes)
    disk size: 728 GiB
    Format specific information:
        extent size hint: 1048576
```  

And check the partition map makes sense:  
```
sudo modprobe -i nbd
sudo qemu-nbd -n -r -c /dev/nbd0 Windows.qcow2

sudo fdisk -l /dev/nbd0
Disk /dev/nbd0: 1.86 TiB, 2048408248320 bytes, 4000797360 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 131072 bytes
Disklabel type: gpt
Disk identifier: 5DFD9739-AC1D-420C-8AB9-7C69DD2A4571

Device           Start        End    Sectors  Size Type
/dev/nbd0p1       2048     534527     532480  260M EFI System
/dev/nbd0p2     534528     567295      32768   16M Microsoft reserved
/dev/nbd0p3     567296 3931336703 3930769408  1.8T Microsoft basic data
/dev/nbd0p4 3931336704 3933677567    2340864  1.1G Windows recovery environment
/dev/nbd0p5 3933677568 3935774719    2097152    1G Microsoft basic data
/dev/nbd0p6 3935774720 4000786431   65011712   31G Microsoft basic data
```

# Create a VM with your image and inject the virtio drivers

It's very likely that the image as it stands isn't bootable, even if you set it up with UEFI.  
Personally, the image had two issues: **Missing KVM drivers**, and a **busted EFI bootloader** partition.  
So the following steps are meant to get you to a bootable VM after creation.  

If you sideloaded the KVM drivers at snapshot time, you might not need to do all that, but I haven't tried it so 🤷  
When creating the VM, assign two CD images to it: A Windows installer disk, and the KVM driver disk.

```
sudo virt-install --name virtual-windows --memory 32000 --vcpus 8 --cpu host --os-variant=win10 \
--features kvm_hidden=on --machine q35 \
--cdrom=ISOs/Win11_24H2_x64.iso \
--cdrom=ISOs/virtio-win.iso \ 
--disk path=Windows.qcow2,size=100,bus=virtio,format=qcow2 \
--boot uefi --graphics spice --channel spicevmc --video qxl --network network=default,model=virtio --noautoconsole \
--features hyperv_relaxed=on,hyperv_vapic=on,hyperv_spinlocks=on,hyperv_spinlocks_retries=8191 
```  

## Sidequest: Accessing the VM remotely
By default KVM allows you to access the VM via SPICE, but only locally. If you're running all this on your homelab, you'll need to edit the VM settings like so:  

```xml
virsh edit virtual-windows  

<!-- Edit the following to have the spice server listen for remote connections; You might also want to add in a password in this case. -->
<graphics type='spice' autoport='yes' listen='0.0.0.0'>
    <listen type='address' address='0.0.0.0'/>
    <image compression='off'/>
</graphics>
```  

Boot to the Windows installer and use it to get a command line going.  
![](https://www.winhelponline.com/blog/wp-content/uploads/2016/05/winre%20(3).png)  

You'll likely notice if you run `diskpart` that Windows doesn't see your VM's disk.  
This can be solved by loading in the virtio storage driver (assuming the CD for it is in the D: drive):  

```
drvload D:\viostor\w11\amd64\viostor.inf
```  

Once you have that and the disk shows up, you can sideload the same storage driver to the VM:  
```
dism /Image:C:\ /Add-Driver /Driver:D:\viostor\w11\amd64
```

# Repair the EFI bootloader 

(This is basically a copypaste of [this article](https://www.winhelponline.com/blog/rebuild-efi-partition-bcd-boot-files/))  
At this stage, you can verify if Windows will boot as-is by running `bcdedit` -- If that gives you an error, you likely need to remake the EFI partition.  

Use diskpart to find the EFI partition (will be around 200 megs), and assign it a drive letter. (partition 3 / drive Y: here)  
```
diskpart
list disk
select disk 0
list partition
select volume 3
assign letter=y
exit
```  

Wipe the partition, then rebuild the bootloader in there:  
```
format y: /fs:FAT32 /q
bcdboot C\Windows /s Y: /f UEFI
```

After all that, `bcdedit` should show the correct boot order, pointed at your C: drive.  
Just reboot the VM and you should be good to go! You'll likely want to install the rest of the virtIO drivers from D: once you make it into Windows.    
