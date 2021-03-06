Title: Masquerading a WSL Distro as a Windows Port, Part 1
Date: 2019-06-05 00:00
Category: LANraragi
Tags: wsl, github actions
Slug: wsl-karen-1
Authors: Difegue
HeroImage: images/karen.jpg
Summary: That's cheating! But is it really seamless?

One of the major complaints I often get with [LANraragi](https://github.com/Difegue/LANraragi) is that it's a major pain to install. And I tend to agree!  
The software runs as a web server through [Mojolicious](http://mojolicious.org), paired with a Redis database.  

Thanks to the power of Docker images, I've made it much easier for Linux users, but Windows users were still stuck dealing with Virtual Machines or the handy-but-not-really-stable [Docker for Windows.](https://docs.docker.com/docker-for-windows/) (Which is pretty much a VM too, all things considered.)  

I got requests for a good Windows version often enough that at one brief point I hacked up a full source port of the app:  
![peak 2016 here lads]({static}/images/quickstarter.jpg)  
It relied on a Redis port [made and subsequently abandoned by Microsoft](https://github.com/microsoftarchive/redis), and a **lot** of batch file glue.  
Lovely, but hey it worked! Until some dude strolled along with his Shift-JIS encoded Windows OS and subsequently broke the entire archive detection code.  
![i fucking hate codepages]({static}/images/coolmeme.jpg)  
Then Mojolicious itself dropped Windows support, things happened, and I pretty much had to kill the thing because it wasn't even standing on its own anymore.  

Meanwhile, [WSL](https://docs.microsoft.com/en-us/windows/wsl/about) was making headlines. I've been using it for a while already to do dev work on LANraragi and it's solid. I read [this blogpost](https://medium.com/@hoxunn/wsl-docker-custom-distro-2-0-730fd97fe72e) recently, which put a crazy and certainly unintended spin on the concept in my head:  

## Why not just ship WSL as a Windows port?

Generating lightweight WSL distros out of Docker images seemed easy with my current workflow, and past that it'd just be a matter of providing users an easy, Windows-like interface to the server stowed away in the distro.  

I'd basically have three big parts to work on for this:  

* 👉 **Build** a WSL distro (basically just a Linux rootfs) out of my existing Docker image  
* 👉 **Register** said distro on the user's computer through the WSL API, and install a basic GUI tool  
* 👉 Use the GUI tool to **interop** with the distro, mapping Windows directories and settings to the Linux world and starting the webserver  

I'll spoil you the results by saying it _totally heckin' works_ and is currently out in beta:  
![bazinger z]({static}/images/karen.jpg)  

One codebase, putting out Docker images used by both Linux and Windows users in "slightly" different ways.  
I'll dedicate the rest of this blogpost - and its followup - to depicting the major hiccups I encountered building this thing out.

# Building the WSL distro in Github Actions  

I do all the continuous integration for LANraragi in [Github Actions](https://github.com/features/actions) these days, so it seemed an easy choice to add the WSL distro build to it.  
According to Nunix's blogpost, it's really just a matter of running [`docker export`](https://docs.docker.com/engine/reference/commandline/export/) on the images I'm already building.  
Said command gives out a .tar containing the full Linux filesystem, for readymade import into WSL. Should be easy, righ-
~~~~
Error response from daemon: This Docker operation is forbidden by GitHub Actions,
you can find documentation at https://developer.github.com/actions/
~~~~
There's actually no warning about this anywhere in the Actions documentation, but since Actions run in premade Docker environments, a few Docker commands are [locked out](https://github.com/actions/docker/issues/7#issuecomment-459808907) to prevent potential sandbox escapes.  

And of course, the all-essential `export` is part of those. I had to switch to using [`docker save`](https://docs.docker.com/engine/reference/commandline/save/), which also exports your image as a .tar archive, but **not** as a ready-to-use filesystem.  
Instead, it exports each layer of the Docker image as a separate .tar, then bundles up all of those.  

![bazinger z]({static}/images/export_vs_save.png)  
This is convenient for reimporting into Docker itself, but not at all for what I want here.  

The hackjob solution I ended up using was to manually squash all the layers post-save:  

~~~~
# Export image and extract the resulting tarball
docker save --output save.tar difegue/lanraragi
tar -xf save.tar --wildcards "*.tar"
mkdir squashed

# Find all .tar files, and export them to the same squashed folder, then repack this as a .tar
find . -mindepth 2 -type f -iname "*.tar" -print0 -exec tar -xf {} -C squashed \; 
find squashed -printf "%P\n" -type f -o -type l -o -type d | tar -cf package.tar --no-recursion -C squashed -T -
~~~~  

Well, got my distro. What now?

# Installing a WSL distro seamlessly to the enduser's machine

Unlike with my previous foray, I didn't(couldn't) bother supporting Windows 7 or 8 here.  
It's straight bleedin' edge Windows 10, which means **PowerShell** is free game instead of wrangling old .bat scripts.  

You can check the full source for the install/uninstall scripts [here](https://github.com/Difegue/Karen/blob/master/Karen/Karen-Installer.ps1)  and [here.](https://github.com/Difegue/Karen/blob/master/Karen/Karen-Uninstaller.ps1)  
I haven't bothered wrapping those in proper executable installers yet: Writing .MSIs is a pain!  
(I don't envy macOS devs often, but I sure could use something like [Platypus](https://sveinbjorn.org/platypus) to quickly wrap scripts in nice-looking executables.)

I initially wrote the scripts fully using `wsl.exe` to unregister/register/terminate the LANraragi distro, but quickly realized that as nice as `wsl.exe` was, it's completely useless in Windows 10 versions under 1903, the April 2019 Update.  
Here's a quick breakdown of available WSL command tools in Win10 and their featureset alongside versions.  

| Win10 version/Tool  | wsl.exe                                                      | wslconfig.exe                            | wslapi.h (direct API call)                  | lxrun                                   |
|---------------------|--------------------------------------------------------------|------------------------------------------|---------------------------------------------|-----------------------------------------|
| 1709 (Fall CU)      | Execute commands in a distro                                 | List distros, unregister, set as default | List, register/unregister, execute commands | (Ubuntu only) Install/Uninstall, Update |
| 1803 (RS4)          | Nothing new                                                  | Nothing new                              | Nothing new                                 | Dead                                    |
| 1809 (RS5)          | Nothing new                                                  | Terminate a running distro               | Nothing new                                 | Dead                                    |
| 1903 (You are here) | List distros, register/unregister, terminate, set as default | Nothing new                              | Nothing new                                 | Dead                                    |  

"Registering" a distro in WSL terms means basically unpacking the Linux filesystem somewhere and registering the resulting folder as containing a Linux distribution.  

`wslconfig.exe` is a more capable alternative for older Windows versions, but it doesn't allow registering a distro.  
As for direct API calls, the [registration function](https://docs.microsoft.com/en-us/windows/desktop/api/wslapi/nf-wslapi-wslregisterdistribution) doesn't allow you to pick a folder to unpack the distro to.  

Since I wanted to target at least 1803, the latest LTSC release, I ended up bundling [LxRunOffline](https://github.com/DDoSolitary/LxRunOffline) alongside the installer to perform the distro registration easily. It also features a nice progress bar `wsl.exe` doesn't have, so at least it looks good. 👀  

![lookin cool unspecified open source software to use on wsl]({static}/images/ps.png)  

Past this, I'm basically just doing usual Installer-y things: Copying the GUI executable to a designated folder in AppData, adding a Start Menu shortcut, checking WSL is installed and that we're on a 64-bit OS, the works.

More on the GUI tool itself in the [next blog post!]({static}/wsl-karen-2.html)
