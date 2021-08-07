Title: Announcing Stylophone v2
Date: 2021-08-23 00:00  
Category: Software  
Tags: mpd, winui, c#, uwp, windows, windows 10, windows 11, music, client, stylophone
Slug: stylophone-2
Authors: Difegue  
HeroImage: images/stylophone/v2-stylohero.jpg  
Summary: Timing both a visual refresh and a major refactoring in one? Don't mind if I do.  

[Stylophone](./stylophone) has been out for almost a year now, and has received as warm a welcome as I could've hoped in the (very) niche world of MPD clients.  
There's been more than 400 trials, and about 100 paid users, which makes this the first time I got any significant form of money from the Microsoft Store. 💰💰💰  

Version 2 of the app has been in the works for a few months already, as I was expecting some form of rejuvenation in the UWP space due to WinUI 3/Windows App SDK.   
The [Windows 11](https://blogs.windows.com/windowsexperience/2021/06/24/introducing-windows-11/) announcement delivered all of that and some!

![Please do not dunk on my music tastes too hard]({static}/images/stylophone/v2-stylophone.jpg)  

As a part of [Launch 2021](https://uwpcommunity.com/launch/), I'm releasing **Stylophone v2**, featuring :  

- A fully rebuilt app, eliminating a bunch of bugs
- Complete restyling using WinUI 2.6 (The bottom area is finally not stuck in dark theme anymore 🙏)
- Support for password-protected MPD servers  
- **Local Playback** if your server has the httpd stream output enabled  
- Random shuffling of tracks from your library into the play queue  

V2 is now **live** on [GitHub](https://github.com/Difegue/Stylophone) and on the [Microsoft Store](https://www.microsoft.com/store/apps/9NCB693428T8)! I'll be rambling a bit more about what I did below.  

# Windows 11 Redesign  

In v2, I spaced most of the UI elements further, both to fit the new card-inspired design language of Windows 11 and to give some elements the extra breathing room they really needed.  
<sub>(Those image comparison sliders are iframes! If they're not showing up your browser might be blocking 'em for some reason. 🤔)</sub>  
<iframe frameborder="0" class="juxtapose" width="100%" height="640" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=43f0a5f0-f7b9-11eb-abb7-b9a7ff2ee17c"></iframe>  
v1's playback controls always felt borderline-claustrophobic to me, with the time slider _almost_ touching both the Play/Pause buttons and the window border.  
This comes at the loss of a bit of vertical space for the content, but I felt it was fine. (And if it's not, you can always enable compact sizing in the settings!)  

<iframe frameborder="0" class="juxtapose" width="100%" height="640" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=c567f9a8-f7b9-11eb-abb7-b9a7ff2ee17c"></iframe>  
This time around, I've mostly <strike>copied</strike> looked at the revamped Settings and Microsoft Store for inspiration. (There's not much else in terms of released WinUI 2.6 apps at the moment. 😛)  

<center>![well at leasy it's not that weird S everyone used to draw in middle school]({static}/images/stylophone/v2-icon.png)</center>  
I've also updated the icon! I liked v1's icon a lot, but it looked a bit too much like the MS Office icons. (A [recurring](https://www.microsoft.com/en-gb/p/quarrel-unofficial-discord-client/9nbrwj777c8r) theme for [third-party](https://www.microsoft.com/fr-fr/p/flowpad/9pmt6j2wvb10?rtc) Fluent Design [apps](https://www.microsoft.com/fr-fr/p/yugen-mosaic/9pf0s24cx0d4) at the time for some reason)   

 
It also looked kinda muddy at small sizes, so I've cleared it up and changed the shape to something...still generic, but more legible at small sizes. The "S" is much less noticeable, which I think is fine since it's kinda just a signature.  

![Comparison of the icons in the new Win11 Start Menu]({static}/images/stylophone/v2-iconstart.png)  

If you preferred the old icon, well, how about buying [a sticker of it](https://ko-fi.com/s/9fcf421b6e) to reminisce about the good old days? 😉  

# (Re)building the app

The structure of the app has switched from **2** projects to about **5**:  
Alongside the existing _MpcNET_ library that's used to handle all the communication with MPD servers and the UWP project itself, I've split most of the core business functionality into a separate _.NET Standard_ class library, which can be reused outside of UWP easily. (More on that later)  
<img src="{static}/images/stylophone/v2-structure.jpg" style="width:468px" />  
Achieving this was relatively easy(albeit time-consuming), as the app already uses the MVVM paradigm through the Community Toolkit's [MVVM library.](https://docs.microsoft.com/en-us/windows/communitytoolkit/mvvm/introduction)  
The major switch I made was to use **Dependency Injection**, which allows me to easily use the OS-specific services within the common ViewModel code, by simply injecting them as implementing the interface.  

![Under the Sycamore treee-wait crap wrong franchise]({static}/images/stylophone/v2-stylophone2.jpg)  

Another big change I made was to handle all the album art decoding and storage in the .NET Standard portion of the code, using [SkiaSharp.](https://github.com/mono/SkiaSharp)  
This allows me to **greatly** cut into the amount of Dispatcher calls I had to make to use the native/UWP image functions, at no real performance loss. (And a great improvement to code readability.)  

The new **Local Playback** feature relies on the MPD server's [_httpd_](https://mpd.readthedocs.io/en/latest/plugins.html#httpd) output, which makes a nice stream we can consume and play back on the Windows machine.  
I used the UWP `MediaPlayer` for this, which does the job well enough. Your mileage with this feature may vary, as I sadly have no way to figure out the encoding used by the server and use its default, which is `ogg`.  

# Ports?

As said above, I rebuilt the entire app to have as much .NET Standard code as possible.  
The main goal behind this was to **port the app** to other platforms. I tried [Uno Platform](https://platform.uno), sadly walked back dissatisfied with the results (forced solution structure, lots of time wasted installing nuget package clones, etc), and tried elsewhere.  

👉 My first look was at Xamarin Forms/MAUI: I quickly reached a working prototype but felt I wouldn't be happy with the UI options available and stopped there. (Besides, I don't really care about Android) 
![ah yes, good old boring material design v1]({static}/images/stylophone/v2-xamarinforms.jpg)  
👉 I briefly considered [Avalonia](https://avaloniaui.net/), but I generally don't like UI frameworks that don't try to look native to the platform they're running on. (This has been greatly improved recently! I might take another stab at it one day.)  

👉 In the end, I decided to try a port to **iOS/UIKit**, using [Xamarin.iOS](https://github.com/xamarin/xamarin-macios) whose macOS variant I was already familiar with.  
Y'know, just 'cause it'd be funny to port a UWP app to run on Apple's own twist on Universal Apps.  

![my brain is about 200 years old probably]({static}/images/stylophone/v2-uikit.jpg)  

As you might see, I got a lot further with this port!  
This is all native iOS UI, powered by the **same** .NET Standard core as the UWP app.  
I learned iOS development from scratch while doing this, which probably led to some bad decisions on the way. 😛  

![never stopping with the bowie references]({static}/images/stylophone/v2-uikit3.jpg)  

This is where I'd normally drop a surprise App Store link, but I'm not sure if the app actually looks good enough/would be successful on Apple devices?    
<sup><sub>And if I'd eventually make back the 90$ a year Apple charges for a developer license, good lord Microsoft has spoiled me with the one-time 100$ payment which I didn't even pay since I got a student deal back in 2013</sub></sup>  
So, consider those screenshots kind of a pitch from me for the time being. 😅  

It's [open source](https://github.com/Difegue/Stylophone/tree/dev/Sources/Stylophone.iOS) just like the UWP variant, so if you like what you see, compile it and give it a try! It's about 80% finished.  
I might come back to it when Xamarin adds support for [Mac Catalyst](https://github.com/xamarin/xamarin-macios/issues/6210), as it'd allow me to target three platforms with this port.  

# Closing words  

Some line of code counts! It's not really a meaningful metric but it's fun:   

Project | LoC (C# only)
-- | --
.NET Standard | 4963
UWP | 3111
iOS/Xamarin | 4537

The UIKit port needed a bit more glue code than I was expecting since unlike macOS/AppKit, UIKit doesn't really have a simple way to do data binding.  
(I'm aware of [Combine](https://developer.apple.com/documentation/combine), but Xamarin.iOS doesn't really allow you to write Swift at the time. 😔)  
![The iOS UI is all storyboards btw, they're polarizing but I like em]({static}/images/stylophone/v2-uikit2.jpg)  
iOS has slide actions on rows which I find really cool and never really used before -- I think it's a bit too hard for users to find out about, though. 😐  
