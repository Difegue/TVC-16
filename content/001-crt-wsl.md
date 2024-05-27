Title: Running cool-retro-term in Windows through WSL1
Date: 2019-04-21 20:00
Category: Cool Tricks
Tags: wsl, cool-retro-term, xming, terminal, crt
Slug: cool-retro-term-wsl
Authors: Difegue
HeroImage: images/crt-win.jpg
Summary: Javascript terminal emulators have nothing on this.

# 2022 Update 

Check [this article](./cool-retro-term-wsl2.html) for updated and much simpler instructions using WSL2+WSLg. 🥳  
Or you can keep reading below if you're stuck with WSL1 for some reason.  

I often work with Linux environments through SSH on my Windows machine. As most people who use the command line on a semi-regular basis, I like looking at available alternatives/customizations to the stock terminal emulator.  


On Windows, you've got a lot of solid alternatives such as cmder or the myriad of cool-looking emulators using web technologies under the hood. (I especially like [Fluent Terminal](https://github.com/felixse/FluentTerminal), which really gets my Win10 design language boner going!)  

But this stuff man, it doesn't have the _bling_. The _hipster cred_.  
![whoa dude now this is good stuff]({static}/images/crt-intro.png)  

[cool-retro-term](https://github.com/Swordfish90/cool-retro-term) is a terminal emulator I often wished I had on Windows, for no other reason than to look cool. Nobody really ever bothered to port it to run on Windows however(and I wouldn't do it either tbh), so I swallowed my dreams of being an _epic hacker_ and just opened up PuTTY for the umpteenth time.  

Until now.  
![bazinga]({static}/images/crt-win.jpg)  

The Windows Subsystem for Linux nowadays just allows one to run the original emulator as-is with a simple X server port for Windows. I'll be giving a short how-to list here, tested on Windows 10 1809.

# Activate WSL and download the required Linux dependencies
I'll let [Microsoft speak for me](https://docs.microsoft.com/en-us/windows/wsl/install-win10) on the first point. I used Ubuntu as a base distro, but you can probably manage with another one.  
Once in your WSL terminal, install the few dependencies you'll need:

~~~~
sudo apt-get update
sudo apt-get install libgl1 xfce4-terminal
~~~~

xfce4-terminal is a hefty download, but without it I was unable to get keyboard input to work in CRT. The errors were linked to XKB, so you might be able to manage by only installing xkb-data or similar packages.  

# Download the cool-retro-term AppImage and extract it
The AppImage conveniently bundles up Qt and everything needed. WSL doesn't have fuse support however, so you'll have to extract it instead of running it as-is. 
~~~~
wget https://github.com/Swordfish90/cool-retro-term/releases/download/1.1.1/Cool-Retro-Term-1.1.1-x86_64.AppImage
chmod a+x Cool-Retro-Term-1.1.1-x86_64.AppImage
./Cool-Retro-Term-1.1.1-x86_64.AppImage --appimage-extract
~~~~
Close your Linux CLI for now.

# Boot 'er up with Xming
👉 Download and install [Xming](https://sourceforge.net/projects/xming/) on the Windows side.  

vcXsrv is another port of the X server to Windows that's often recommended in [X-on-WSL blogposts](https://www.ctrl.blog/entry/how-to-x-on-wsl), but it didn't work with CRT during my experiments. You can also try [FreeXer](https://sourceforge.net/projects/freexer/), or Cygwin's X server.  

Once installed, just start it up and go back to Linux:  
~~~~
export DISPLAY=:0
cd squashfs-root
./AppRun
~~~~

![lookin' hefty on cpu joker]({static}/images/crt-cpu.jpg)  
From here on, you can right-click on the terminal to load a different graphical profile or make a custom one yourself.  
Basically everything works as-is -- even urxvt mouse tracking!

# Automating it all with some scripting

I jerry-rigged a pair of .bat/.sh scripts to start both Xming on the Windows side and CRT on the WSL side.

**cool-retro-term.bat**
~~~~
start "" "C:\Program Files (x86)\Xming\Xming.exe" :0 -clipboard -multiwindow
start /min wsl -d ubuntu ./crt.sh
~~~~

**crt.sh**
~~~~
cd ~/squashfs-root && export DISPLAY=:0.0 && ./AppRun 
~~~~

# Caveats

* WSL [doesn't have GPU acceleration yet](https://github.com/Microsoft/WSL/issues/829). This is entirely running in software and as you can see in the `htop` above, easily eats more CPU than those newfangled javascript terminals. 😐 
* Pasting text into cool-retro-term works, but copying text from it doesn't. 
* You can encounter a segfault or two if you mess with the graphical settings too much in one session. Once a profile is saved however, I've encountered no crashes in the few hours I spent playing with this.

All things considered, this is basically a party trick at the moment and nothing else.  
It's pretty cool with `ncmpcpp` though!
