Title: Masquerading a WSL Distro as a Windows Port, Part 2
Date: 2019-06-06 00:00
Modified: 2019-06-06 00:00
Category: LANraragi
Tags: wsl, wpf, c#
Slug: wsl-karen-2
Authors: Difegue
Summary: Interacting with WSL from managed code isn't as easy as I'd thought.

[Previously,]({static}/wsl-karen-1) we got to the point where we had a WSL distro installed seamlessly to the user's computer, alongside all the shortcuts, bells and whistles of a proper Windows application.  
Let's talk a bit about the Windows GUI part of the magic trick.  

## A simple, taskbar-based GUI  

Since the bulk of the interaction with LANraragi won't be made from this GUI, I wanted to make it as unobtrusive as possible, while still featuring some [Fluent Design](https://www.microsoft.com/design/fluent/).  

I got some inspiration from Docker for Windows' [welcome screen](https://docs.docker.com/docker-for-windows/images/docker-app-welcome.png) and the OneDrive app in W10, who both pop-up small windows from their tray icons.

![light themin']({static}/images/karen-light.jpg)  

I rolled [this handy](https://www.nuget.org/packages/Hardcodet.NotifyIcon.Wpf/) NuGet package to get the tray icon part out of the way and got to work designin'.  

Fluent Design would've been almighty easy to pull off had I used [XAML Islands](https://docs.microsoft.com/en-us/windows/apps/desktop/modernize/xaml-islands), but I didn't want to be **too** bleeding edge and restrict the app to 1903 and up purely for cool visual effects. Maybe in a few years. 🏝   

Instead, I rolled Acrylic the [DIY way](https://withinrafael.com/2018/02/01/adding-acrylic-blur-to-your-windows-10-apps-redstone-4-desktop-apps/), and Dark Theme by [looking up the registry.](https://engy.us/blog/2018/10/20/dark-theme-in-wpf/) The buttons are just some custom XAML [theming](https://github.com/Difegue/Karen/blob/master/Karen/App.xaml#L69).  

The final result is probably overkill for an interface most people will only look at for 5 seconds, but I couldn't help it. 

## WSL interop from WPF

The GUI interops with WSL in four different ways.  
I expected to use the [WSL API](https://docs.microsoft.com/en-us/windows/desktop/api/_wsl/) to do all of these with P/Invokes galore, but encountered a few hitches where I had to run `wslconfig.exe` and `wsl.exe` instead through NET's Process API.

### 🐧 Check that the Linux Distro is actually installed

`WslIsDistributionRegistered` flat out [doesn't work](https://stackoverflow.com/questions/55681500/why-did-wslapi-suddenly-stop-working-in-wpf-applications) in a GUI application for now. I had to make due with running `wslconfig.exe /l` and parsing its output to find my distro name.  

(I initially toyed with the idea of being able to uninstall/install the Distro from the GUI using `WslRegisterDistribution`, which would allow for easy updates, but not being able to specify the folder the distro lands in kinda put a stop to that.)

### 🐱‍💻 Execute a Perl one-liner to fetch the LANraragi Version number installed in it

Using some [ojo](https://mojolicious.org/perldoc/ojo) magic ⚡⚡⚡ :
~~~~bash
perl -Mojo -E "my $conf = eval(f(qw(/home/koyomi/lanraragi/lrr.conf))->slurp); say %$conf{version}.q/ - '/.%$conf{version_name}.q/'/ "
~~~~

This version is then displayed on the GUI.  
I **could've** used `WslLaunch` here to run my one-liner, but the function requires a rather hefty baggage to get started(more on that later). The `WslLaunchInteractive` variant just works, but it pops up a console and we don't want any of that.  

Instead, I simply run my one-liner in `wsl.exe` and fetch the text result.

### 📂 Set up a symbolic link to the content folder specified in the GUI

When the user gives us his content folder, it's a pure Windows path.   
I quickly convert it to its WSL equivalent and setup a symlink to a designated folder in the Linux filesystem:  

~~~~c#
// Map the user's content folder to its WSL equivalent
// This means lowercasing the drive letter, removing the : and replacing every \ by a /.
string winPath = Properties.Settings.Default.ContentFolder;
string contentFolder = "/mnt/" + Char.ToLowerInvariant(winPath[0]) + winPath.Substring(1).Replace(":", "").Replace("\\", "/");
~~~~

### 🆙 Start and stop the Linux server

* `WslLaunch` is used to start the server. I use the same customized init system as in my Docker images, so all the setup save for the symlinks done above is already there. The function requires opened STDIN/STDOUT/STDERR streams to pipe the process into, so I [create a hidden console](https://docs.microsoft.com/en-us/windows/console/allocconsole) to magically give my GUI usable console streams.

* There's no API function available to terminate/stop a currently running WSL distro. While `WslLaunch` gives you the PID of the process you start in WSL, Linux processes aren't hard-tethered to their parents. I always seemed to get a bunch of child processes laying around even after killing said PID, so I added a call to `wslconfig.exe /t` to the mix.

Using an extra [NuGet](https://www.nuget.org/packages/HideConsoleOnClose/) package, I got a user-friendly Log Console without even really trying at all. 🥤😎

![it's not WSL without a terminal hidden somewhere is it]({static}/images/karen-dark.jpg)  

This is just the console created from `AllocConsole`, shown and hidden when the user clicks the "Log Console" button. The NuGet package adds some extra sorcery to make sure closing the console simply hides it again.

## Final thoughts 

Packing up an entire WSL distribution seemed way too clumsy to pull off at first, but Microsoft's tooling actually makes disposable distros pretty easy to do! I could almost put this on the store if it wasn't for the fact I'm horribly twisting what WSL was originally made for. _Please forgive me Rich Turner for I have sinned_  

My Docker images are pretty lightweight since I went all in on Alpine a few months back, so the full downloadable Windows package clocks in at **85 MBs**, with a few more optimizations possible in the future.  
That's less than your average Electron application. 😏  
