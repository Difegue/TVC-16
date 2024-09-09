Title: The Stylophone 2.7 Update is here! 
Date: 2024-09-09 00:00  
Category: Software  
Tags: mpd, xamarin, dotnet, c#, uwp, windows, xbox, ios, macos, catalyst, app store, music, client, widgets, stylophone
Slug: stylophone-27
Authors: Difegue  
HeroImage: images/stylophone/v27-catalyst.jpg  
Summary: isn't it kinda stupid to make the free version the one on the platform that users tend to pay for the most?

Another [year](./stylophone-26.html), another Stylophone update!  
This is a smaller update this year, but I still have a few niceties in store -- Most notably, 

# Mac support!  
![Stylophone 2.7 on Sonoma]({static}/images/stylophone/v27-catalyst.jpg)  
As mentioned last time, the Mac Catalyst version finally works, so I took some time to "polish" it up and make it shippable.  

...I say "polish" because at its heart, it's really just the iOS version thrown in Catalyst?  
There are no large Mac-only interface changes here, I'm afraid. 
### It's just too much gat dang work!  

To make up for that though, I've decided to make the macOS version entirely 🫰**free**🫰 - No need to compile it yourself or to get it from an App Store, it's just there for the taking in the [GitHub releases](https://github.com/Difegue/Stylophone/releases/tag/2.7.0).  

I hope you have fun with it! It's signed and notarized so it should just work™️.    

# The other things  

For all platforms, I've mostly gone through some user asks in this release, so:  

- You can now enable/disable specific MPD outputs through Settings
- You can now specify the port of the httpd stream for Local Playback  

That's about it. I didn't really find anything interesting<sup id="ref-1">[*](#note-1)</sup> in iOS17 all things considered, so the app version still just requires iOS16.  

But for Windows, there's a _small bonus_!  
You can now use the `stylophone://` protocol on your PC to launch and control the app. See [here](https://github.com/Difegue/Stylophone#protocol-usage-windows-only) for details.  

This actually comes from another feature I was experimenting on; **Widget support**.  
Widgets are normally a WinUI thing and [kinda suck to support on UWP](https://nicksnettravels.builttoroam.com/uwp-widget/), so I started architecting a two-app solution that could potentially become its own product...  

And it worked! Except the Windows Widget pane actually [still kinda sucks](https://kolektiva.social/@Difegue/113076064804645110) even with the DMA changes.  
![dankpods voice: can you believe no one uses this]({static}/images/stylophone/v27-widget.jpg)  
It's all nice and good to base your widgets on [Adaptive Cards](https://learn.microsoft.com/en-us/windows/apps/design/widgets/widgets-create-a-template) - except as a result you have no support for font icons, light/dark theming sucks, and all your resources need to be URLs<sup id="ref-2">[**](#note-2)</sup>.  

I don't think it's really worth doing anything with the Windows Widget board in its current state unless you're on a Microsoft payroll - Which is probably why no devs outside of Spotify have done so.  

Maybe in a few years when the AI hype weans off and we start getting actual OS features again? I think Widgets could be powerful if they could be perma-anchored to the desktop like macOS does.  

The well might be poisoned already though, since now everyone associates Widgets with the dogshit News features the MSN team crammed into the OS before fucking off to do Bing chat and Bing chat accessories.   

In the meantime, I've made the now playing indicator a squiggly line. everyone loves squiggly lines cmon  
![hell yeah]({static}/images/stylophone/v27-squiggle.png)  

### As usual, the apps can be downloaded from both the [Microsoft Store](https://www.microsoft.com/store/apps/9NCB693428T8?cid=storebadge&ocid=badge) and the [App Store.](https://apps.apple.com/us/app/stylophone/id1644672889?itsct=apps_box_link&itscg=30200)  

I hope you enjoy the updates! Free for existing users as always. Here's the full changelog:  

```
## All platforms
* Add support for listing and enabling/disabling MPD server outputs
* The port of the httpd stream for Local Playback can now be configured.
* Fix some crashes that could happen when selecting an album very quickly after a search (#98)

## macOS
* I am now offering the Mac Catalyst version of Stylophone as a freebie. Feel free to download it below!
* This is a "bare minimum" port of the iOS version to the Mac - Don't expect much, but it's signed/notarized and works just fine.  

## iOS
* Local Playback should now resume when going back to the app after an audio interruption. (#96)

## UWP 
* Stylophone can now be launched through the stylophone:// protocol! This feature also makes it so you can control some features of the app through protocol invocations. See https://github.com/Difegue/Stylophone#protocol-usage-windows-only for more details.  
* Updated the playing item in Queue to use marquee text and a clearer now playing indicator. 

See the full changelog here:
https://github.com/Difegue/Stylophone/compare/2.6.2...2.7.0
```

# Closing thoughts  
![good ol' vsmac..]({static}/images/stylophone/vsmac.png)  
Visual Studio for Mac is dead and buried as of a few days ago, but I still used it to get the iOS update out...  
Since it mostly relies on `dotnet` these days, there's no problem using it with the latest [.NET SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) which works just fine for buildin', debuggin', and gettin' your `.ipa`s out.  

The bitrot will probably get to it next year, but for now? I guess I can enjoy the last Microsoft IDE that doesn't have a bloody chatbot<sup id="ref-3">[***](#note-3)</sup> built into it.  

With the new action button™️ on iPhones now, I should add Shortcuts to the iOS app at some point...  


#

<sup id="note-1">[\*](#ref-1) I mentioned [TipKit](https://bendodson.com/weblog/2023/07/26/tipkit-tutorial/) last time, but turns out that doesn't have any ObjC bindings so it can't be used from Xamarin.. NET9 (finally) has Swift interop support now though, so maybe next year?</sup>  
<sup id="note-2">[\*\*](#ref-2) Taking apart the built-in widgets shows there is **some** support for reading image resources from the full app package? But it's completely undocumented so I had no idea where to start. </sup>  
<sup id="note-3">[\*\*\*](#ref-3) I actually like base copilot for code completion not gonna lie, but the chatbot thing? meh. Where the fuck is VS2024 already? The redesign has been in preview for years at this point </sup>  
