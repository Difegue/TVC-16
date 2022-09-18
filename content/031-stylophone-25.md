Title: Stylophone 2.5 is now out for Windows...and iOS!
Date: 2022-09-17 00:00  
Category: Software  
Tags: mpd, xamarin, dotnet, c#, uwp, windows, ios, app store, music, client, stylophone
Slug: stylophone-25
Authors: Difegue  
HeroImage: images/stylophone/v25-stylohero.jpg  
Summary: I'm coming for **your** dynamic island! 

It only took me [a year](./stylophone-2.html), but Stylophone is finally available on iOS and iPadOS!  

![Stylophone 2.5 on iPad]({static}/images/stylophone/v25-ipad.jpg)  
It looks quite similar to the Windows version, doesn't it?  
![Stylophone 2.5 on Windows]({static}/images/stylophone/v25-win.jpg)  

Version 2.5 is now available on both the _Microsoft Store_ for the UWP version, and the _App Store_ for your iDevices.  
(And of course, still open source on [GitHub](https://github.com/Difegue/Stylophone/releases/tag/2.5.4)!)

[<img src="https://getbadgecdn.azureedge.net/images/en-us%20dark.svg" width="200"/>](https://www.microsoft.com/store/apps/9NCB693428T8?cid=storebadge&ocid=badge) [<img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" width="216"/>](https://apps.apple.com/us/app/stylophone/id1570000000)

Thanks to a common .NET core codebase, both versions are **near-identical** as far as features go.  
<sub>(iOS is missing Queue reordering! That'll come in time.)</sub>  

That includes **Local Playback**, integration with System playback controls, and all that good stuff!  
The new iOS 16 Lockscreen looks particularly snazzy with Stylophone on it:  
<img src="{static}/images/stylophone/v25-lockscreen.jpg" alt="Stylophone 2.5 on the iOS 16 Lock screen" width="300"/>  

# Multiplatform bonanza

I'm pretty stoked about breaking out into Apple Developer land!  
With the combined powers of UWP and UIKit, you can now manage your MPD server using Stylophone on:  

- Windows 10/11 PCs
- Xbox One/Series
- iPhone/iPad
- macOS, if using [Apple Silicon](https://developer.apple.com/macos/iphone-and-ipad-apps/).  
<sub>(Sadly, Apple TV/tvOS isn't as easy to develop for as the Xbox is..)</sub>  

I don't have an ARM Mac to test the app on, but I did try chucking it in [Mac Catalyst](https://developer.apple.com/mac-catalyst/) to see how it'd end up:  
![Please do not dunk on my music tastes too hard]({static}/images/stylophone/v25-catalyst.jpg)  
Doesn't look too bad, and could probably be improved a little bit with some Mac-specific magic!  

Catalyst support required Microsoft.iOS, aka the [new version of Xamarin.iOS](https://github.com/xamarin/xamarin-macios/wiki/.NET-release-notes-Xcode-13.3).  
As that new version changed TFMs, [LibVLC](https://code.videolan.org/videolan/LibVLCSharp/-/issues/346) is currently broken on it; So no Catalyst for now!  

I don't expect to support any additional platforms for the time being; Previous experiments with Uno and MAUI were [painful](https://twitter.com/Difegue/status/1329221609652105217?ref_src=twsrc%5Etfw).  
Xamarin.Android could be an interesting avenue, but I don't feel like developing for Android even though it's my daily driver...    

# The icon changed (again)

If youuuuu can believe it, it's <s>a Friday</s> [Spline](https://spline.design) time once again!  
I've refined the existing icon design by giving it the 3D treatment.  

<img src="{static}/images/stylophone/v25-icon.png" width="256"/>
<sub>Hey, the S from the [v1 icon]({static}/images/stylophone/styloicon.jpg) is back! Can't this guy make up his mind for once?</sub>  

A far cry from the 2020 MS Office ripoff icon -- Playing with materials in 3D is fun!  
Here are a few other iterations and abominations:  
![That lower left one is some Gucci shit I tell you what]({static}/images/stylophone/v25-icontests.png)  

# Closing thoughts  

![funny gnu meme man]({static}/images/rmshacking.png)  
_Actually, we encourage people who redistribute free software to charge as much as they wish or can._  
- [Free Software Foundation](https://www.gnu.org/philosophy/selling.en.html)  

While Stylophone itself is open-source software, I charge for it on both Stores;  
You get _easy updates_, and I get to make back the $99 **[FRUIT COMPUTING COMPANY]** took from me.  

However, to celebrate the iOS release, the UWP/Windows version is currently [**[50% OFF!]**](https://www.microsoft.com/store/apps/9NCB693428T8?cid=storebadge&ocid=badge)  
It also still has a free trial, so you can see if it's a good fit for you/your MPD server setup before buying.  


<sup><sub>...There is no cr[o](https://cutt.ly/LVu1GDo)ss-buy.</sup></sub>  


