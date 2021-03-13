Title: Introducing Stylophone
Date: 2020-09-13 00:00  
Category: Software  
Tags: mpd, winui, c#, uwp, windows, windows 10, music, client
Slug: stylophone
Authors: Difegue  
HeroImage: images/stylophone/stylohero.jpg  
Summary: A modern, native MPD client for the Universal Windows Platform.  

[Music Player Daemon](https://www.musicpd.org/) clients don't get much love on Windows.  
You're usually left with ports of whatever clients people have created for Linux, which usually involves GTK, Qt or other cross-platform control libraries which look like they're coming straight out of the Windows 7 era.  

The only MPD client offering on the Microsoft Store is [Chimney](https://www.microsoft.com/en-us/p/chimney/9wzdncrfj6jx), which I'm pretty sure nobody remembers anymore due to the Store being utterly unsearchable. It works, but the Windows 8 aesthetic feels just as out of place nowadays...
![Circled buttons? What *is* this, Windows Phone 7?]({static}/images/stylophone/chimney.jpg)  

I've used [Cantata](https://github.com/CDrummond/cantata) for a long while as it was the only client left that was sorta-up-to-date, but it recently slipped into maintenance mode.  

[Even macOS](https://persephone.fm/) was getting a brand new native MPD client with Swift 'n bells 'n whistles! Enough!  
Making a new MPD client running on UWP/WinRT was a good way to check out how the platform's evolved since I last made RSS Live Tiles in 2017.  

![Soul Hackers is underrated soundtrack work from Shoji Meguro]({static}/images/stylophone/stylophone.png)  

Stylophone is now **live** on [GitHub](https://github.com/Difegue/Stylophone) and on the [Microsoft Store](https://www.microsoft.com/store/apps/9NCB693428T8), so if you don't really care how the app was made you can stop reading and click on 👆👀☝  

# Building the app

A .NET base for the client section thankfully already existed through [LibMpc.net](https://archive.codeplex.com/?p=libmpc), an ole' codeplex library which got reworked and improved upon through the years [on Github.](https://github.com/glucaci/MpcNET)  
So Stylophone technically contains code from 2008, which is...not very important but nice!  

To bootstrap the UWP app portion, I've been really impressed with the [Windows Template Studio](https://docs.microsoft.com/en-us/windows/uwp/design/windows-template-studio/), which allows you to prop up a skeleton and start coding app functionality straight away without having to reimplement `INotifyPropertyChanged` and `BoolToVisibilityConverter`s for the 9847563th time. A+ stuff.  

I've also used the [Windows Community Toolkit](https://github.com/windows-toolkit/WindowsCommunityToolkit) for a few real nice-to-haves, such as [middle-mouse scrolling](https://github.com/windows-toolkit/WindowsCommunityToolkit/tree/master/Microsoft.Toolkit.Uwp.UI/Extensions/ScrollViewer) and listview headers.  

The architecture is standard MVVM, with a few services for essential features such as navigation and listening to the MPD server through an idle connection.  

# Design and name

Music players often appear in designer concepts, so I had [a lot](https://twitter.com/zeealeid/status/1262382516591345674) of [inspiration](https://twitter.com/ImShashankDogra/status/1144380971485057024) to [choose from](https://twitter.com/define_studio/status/1297163374812266496).  
Even on the [macOS side,](https://twitter.com/jsngr/status/1280619068794470402) since they're also jumping on the "transparent sidebar" bandwagon now.  
<sup><sub>Microsoft always does it first m8s</sub></sup>  

For existing apps, I mostly looked at Groove Music, but also some existing UWP players like [SoundByte](https://github.com/DominicMaas/SoundByteOSS) or [Bread Player.](https://github.com/thecodrr/BreadPlayer)

![Truth is, the compact view is entirely ripped off from SoundByte! God bless open source]({static}/images/stylophone/stylophone2.jpg)  

The app uses WinUI 2 by default, although there are a few parts where I still needed stock Windows.UI.Xaml. (Mostly for background Acrylic)  

The name was "FluentMPC" for the longest time, briefly became "Moroder" before I settled on "[Stylophone](https://en.wikipedia.org/wiki/Stylophone)", referencing the lil' dingus toy instrument David Bowie used in *Space Oddity*.  

![It also served in Heathen(The Rays) which in my opinion is a better Bowie track but I'm probably alone on that]({static}/images/stylophone/styloicon.jpg)  

The look of the instrument made for good inspiration as well when it came to making an icon.  
Starting from the same proportions as the modern office icons, I used the look of the metal latches as the pattern and heavily simplified the "S" from the original logo.  

The resulting icon doesn't indicate whatsoever that this is a music-related application. 🤐  
But as someone who can't design, I like it!  

# Essential features and tailoring the app

What I wanted most from an MPD client besides the obvious playback/playlist features was **good album art handling.**  
Traditionally, MPD clients used to pull album art from outside sources like search engines or last.fm, as the server had no capacity to provide art to clients. This usually led to a bunch of false positives, and allowed said search engines to track what you listened to.  

This changed [recently](https://github.com/MusicPlayerDaemon/MPD/issues/42) with the `albumart` command, which allows clients to pull binary data for cover art from the server.  
It only handles cover.jpg/png files in the same folder as the tracks for now, but a second command, `readpicture`, is stated to come in MPD 0.22 to handle embedded art.  

Stylophone handles both commands to build its album art cache, so it is future-proofed in that sense.  

My second most-wanted "feature", if it can be called that, is a good _Now Playing_ view.  
I'd like to use Stylophone in a smart speaker setup later down the line, where it could show the current/next tracks on a touch screen alongside the basic playback controls.  

![Waiting for the Deadly Premonition 2 soundtrack...]({static}/images/stylophone/stylophone3.jpg)  

# Closing words  

_Actually, we encourage people who redistribute free software to charge as much as they wish or can._  
- [Free Software Foundation](https://www.gnu.org/philosophy/selling.en.html)  

Stylophone currently costs 5 USD on the [Microsoft Store](https://www.microsoft.com/store/apps/9NCB693428T8).  
The entire app is free software under the MIT license so you can just compile it yourself if you don't want to pay. 👌  
I won't provide binaries in any other fashion at the moment since distributing UWP apps is just [annoying.](https://github.com/microsoft/ProjectReunion/issues/128)  
<sup><sub><strike>Although if you've read the article all the way to the end, you might just deserve a [freebie!](http://go.microsoft.com/fwlink/?LinkId=532540&mstoken=CK394-4WW3G-DDJP6-2MC92-WP49Z)</strike> It's over chief the promo code expired might make a new one someday</sup></sub>  


Maybe in a year or so, I'll be able to port the app to Mac, Linux and mobile throught the [Uno Platform](https://platform.uno/blog/announncing-uno-platform-3-0-linux-support-fluent-material-and-more/), giving me total dominion over the MPD client space.  
And endless anguish from having to support users from so many different platforms.  

![John Carmack's inauguration speech has some great thoughts about the current state of computing you should go watch it]({static}/images/coolmeme.jpg)

**late 2020 edit**  
I guess the total dominion thing will have to wait a bit considering how Uno fares at the moment.  

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Tried cramming the Stylophone codebase into Uno Platform and it&#39;s uhhhhhhhhhhhhhhhhhhhhhhhhhhh it can play songs I guess? <a href="https://t.co/ZAmbOaN21E">pic.twitter.com/ZAmbOaN21E</a></p>&mdash; ＫＩＬＬＥＲ ＱＵＥＥＮ (@Difegue) <a href="https://twitter.com/Difegue/status/1329221609652105217?ref_src=twsrc%5Etfw">November 19, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>  
