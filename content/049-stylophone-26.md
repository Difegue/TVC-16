Title: The Stylophone 2.6 Update is here! 
Date: 2023-09-20 00:00  
Category: Software  
Tags: mpd, xamarin, dotnet, c#, uwp, windows, xbox, ios, app store, music, client, stylophone
Slug: stylophone-26
Authors: Difegue  
HeroImage: images/stylophone/v26-iphone.jpg  
Summary: Thank you, Ryuichi Sakamoto.

It's been... [a year](./stylophone-25.html) once again! Wow!   
Now that the [gamedev](./funtography) side of the hustle has quieted down a bit, it's time to get back into the app business.  

In this hectic period of iOS17 app updates, I'm happy to deliver... the **_iOS16_ update** for Stylophone<sup id="ref-1">[*](#note-1)</sup>. 🤲  
`v2.6` is a fairly large update, fixing some longstanding bugs for both iOS and Windows/Xbox.  

The iOS version has freed itself from the shackles of _old_ Xamarin and is now... on [_new_ Xamarin](https://github.com/xamarin/xamarin-macios/wiki/.NET-release-notes-Xcode-13.3), AKA .NET 7.  

The Windows version hasn't budged at all since I still want to support Xboxes<sup id="ref-2">[**](#note-2)</sup>.  
It still got some nice new UI improvements thanks to the recent [Windows Community Toolkit](https://devblogs.microsoft.com/ifdef-windows/announcing-windows-community-toolkit-v8-0/) update, however!  

![Stylophone 2.6 on iPhone]({static}/images/stylophone/v26-iphone.jpg)  

_iOS/iPadOS_ received the blunt of the UI work this time - iPhone users should enjoy much more usable table views now, with edit mode enabled for **quick reorder/deletion**.  
I added a bunch of missing Narrator/VoiceOver hints following reports by a visually impaired user to both versions. Kinda wish I'd gone over that earlier considering how easy it was..

There's some new MPD feature support as well, most notably the new `playlistdelete` range functionality!  
I have made a matching [MpcNET](https://www.nuget.org/packages/MpcNET/) nuget release, in case you want to use that.  

### As usual, the apps can be downloaded from both the [Microsoft Store](https://www.microsoft.com/store/apps/9NCB693428T8?cid=storebadge&ocid=badge) and the [App Store.](https://apps.apple.com/us/app/stylophone/id1644672889?itsct=apps_box_link&itscg=30200)  

I hope you enjoy the updates! Free for existing users as always. Here's the full changelog:  

```

Shared:

    (#75) Fix potential failure in GetColor crashing the album display
    (#39) Add hostname support to the MPD server text field
    (#59) Use "albumsort" instead of album when listing albums in the Library
    (#60) Use "albumartist" in album views when available
    Use the new MPD playlistdelete range feature when removing items from playlists

UWP:

    Migrate to Windows Community Toolkit v8 🎊
    Fix alternate line colors being broken on Windows 11 machines
    Shadows have been revamped across the app.
    A new nicer segmented control has been added to Search results.
    Settings got a small facelift
    Fix the loading bar not showing when cover art is downloading for an album
    The playback slider is now properly controllable via keyboard.
    The app should no longer be suspended by Windows. This fixes various issues regarding connection stability and Xbox background functionality.
    Try/catch potential exception in double-tap to play
    Added missing Narrator hints for the playback views.

iOS:

    The app has migrated to .NET7 🎊 Now requires iOS16.
    Table views have been reworked across the app to show more content in compact mode
    Fixed Table views getting resized incorrectly on phones when switching from portrait to landscape multiple times.
    You can now directly tap to play/add to queue in all table views.
    The old multiselect behavior in album/playlist views has been retired for the time being.
    Queue and Playlists can now be edited/reordered
    Fix a bug where visiting multiple album pages would stack then in the background when clicking "Add to Queue"
    Fixed navigation on phones always taking you back to the Queue before showing the Sidebar.
    Rework NowPlaying View to take into account safe insets properly
    The Add to Playlist dialog has been retooled to take less empty space.
    Non-error in-app notifications are now less intrusive.
    (#73) Added missing VoiceOver hints for the playback views.
```

# Closing thoughts  
![good ol' vsmac..]({static}/images/stylophone/vsmac.png)  
Working on the iOS version of Stylophone means I get to pull out **Visual Studio for Mac**... Which is [dying soon.](https://devblogs.microsoft.com/visualstudio/visual-studio-for-mac-retirement-announcement/)  
I'm gonna miss the thing!  

Sure, it's the red-headed stepchild of regular Visual Studio, built off the back of [MonoDevelop](https://github.com/mono/monodevelop/) without contributing sources back... But I got into macOS/iOS development with it and for all its weird faults and bugs, it was _fine_ and had a decent workflow for Xamarin-based projects.  

It feels especially wasteful considering they [revamped large swaths](https://devblogs.microsoft.com/visualstudio/visual-studio-2022-for-mac-is-now-available/) of it **last year**!  
🤨 What the fuck is Microsoft even _doing_? Did they just fire most of the devs in their godawful layoffs and couldn't keep it going?  

![Please do not dunk on my music tastes too hard]({static}/images/stylophone/v25-catalyst.jpg)  

On the flipside, having moved to NET7 gives me access to Mac Catalyst builds of Stylophone again...  
There are [great native](https://github.com/danbee/persephone) MPD clients for macOS already, but I might release that as a freebie version later.  
  
Maybe even with iOS16 goodies thrown in!  
  
...If the xamarin platform doesn't keel over and die in the meantime<sup id="ref-3">[***](#note-3)</sup>.


#

<sup id="note-1">[\*](#ref-1) I really wanted to use [TipKit](https://bendodson.com/weblog/2023/07/26/tipkit-tutorial/), but the xamarin bindings probably won't be ready for another few months... Them be the woes of cross-platform development.</sup>  
<sup id="note-2">[\*\*](#ref-2) which hopefully will be more usable now that I'm using the ol' silent .wav technique to prevent the app from being background killed 😎😎</sup>  
<sup id="note-3">[\*\*\*](#ref-3) Also my mac mini doesn't support Ventura and I already had to hack the minversion to get Xcode 14.3 to run sooo </sup>  
