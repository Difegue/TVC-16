Title: Fixing an Apple Performa Plus CRT Display
Date: 2019-12-27 00:00  
Category: Hardware  
Tags: apple, macintosh, mac, performa, crt, diy, retrocomputing
Slug: performa-plus-display
Authors: Difegue  
HeroImage: images/performa/performa8.jpg
Summary: I ain't afraid of no CRT.  

![domo watashi wa performa-san desu]({static}/images/performa/performa.jpg)  
This is an Apple Performa Plus Display. It's...a completely standard Shadow Mask CRT.  
```
The Apple Performa Plus Display was a low-end Goldstar-built 14-inch monitor designed and fabricated for the Macintosh Performa series. Apple slightly modified this device to create the Apple Color Plus monitor, which was essentially the Performa Plus Display in a nicer case. The Apple Performa Plus Display also had a tilt & swivel stand.
```  
I liked the size though, so I grabbed it! Only issue is that its cable was cut off.  
![this is fucking barbaric but what do you expect out of a screen with no detachable cable]({static}/images/performa/performa2.jpg)

The tube seemed to work fine when powered on, although there's no real way to make sure without feeding it a proper video signal! What the hell, let's take it apart.  
![dude it's alright CRTs can't kill yo-*dies in flyback transformer*]({static}/images/performa/performa3.jpg)  

The inside circuit looked pretty much perfect -- No blown caps or anything weird that'd have made me give up on the spot.  
What I'm interested in is the internal video connector here, which is at the other end of the cut-off cable:  

![wish I had a time machine to '94 to ask apple/goldstar engineers why the ground isn't in the connector]({static}/images/performa/performa4.jpg)  
Of course, there's no detailed information on the net about the pinout of an internal video connector for a one-off CRT monitor.  
The Service Manual certainly doesn't help either:  
![haha yeah fuck you apple]({static}/images/performa/performaservice.png)  
So, how am I going to remake the cable for this thing?  

# Technotes to the rescue  

```
Technical Notes provide late breaking information about new Apple technologies and supplementary documentation discussing some of the more complex issues related to programming for the Mac OS.
```  
I was surprised to see that old Mac hardware is actually quite well documented thanks to Apple's old [technotes](https://developer.apple.com/library/archive/navigation/#).  
I used a [mirror from 2002](https://www.fenestrated.net/mac/mirrors/Apple%20Technotes%20(As%20of%202002)/) to shorten a bit the amount of articles I had to search/read through, but you can certainly pull all the info you need from the official site.  

Looking at the [Color Monitor Connections](https://www.fenestrated.net/mac/mirrors/Apple%20Technotes%20(As%20of%202002)/hw/hw_08.html) article basically gave me all the info I needed.  
Since this is Apple, Macintosh screens don't use classic VGA but DA-15 connectors with a custom pinout:  
![Macintosh II Video Card and Macintosh IIci Built-in Video]({static}/images/performa/mac_video.gif)  
Looking at this pinout and the way the cables are laid out/colored in the internal video connector, you can theorize a mapping. Let's look back at what is in the CRT:  

* The red/blue/white wires are each paired with a matching ground(black) wire.
* After that, there is only one brown wire and two black wires left.
* The chassis (global) ground isn't even on the connector, making it rather obvious.  

It's easy to guess that the pairs of red/blue/white match the color signals (`RED/RED.GND`, `BLU/BLU.GND`, etc.). <sup><sub>It's a bit weird that Green is represented by a white wire, I guess they didn't have green ? </sup></sub>  
What about the brown wire, though?  

The last piece of the puzzle is that Mac screens don't use Horizontal/Vertical Sync like VGA, instead preferring to use [Composite Sync](https://en.wikipedia.org/wiki/Component_video_sync).  
The DA-15 pinout above has pins for VGA-style `HSYNC/VSYNC`, but those are meant for those not-at-all common cases where you'd hook up a VGA screen to your Mac with an adapter.  

Therefore, there are only **two** wires to hook up for the Sync signal (`CSYNC` and `CSYNC.GND`), instead of the four for VGA.(`HSYNC/VSYNC` and their matching grounds)  
It seems then likely that the brown wire is the `CSYNC` signal!  

### But aren't you missing some pins from the DA-15 picture?

I am! I didn't talk about `SENSE0/1/2` yet.  
Those pins are meant to be grounded in specific ways to tell the Mac what kind of screen we're plugging in. For example:  
```
The Macintosh LC requires that pin 4 (SENSE0) be connected to Ground to signal the connection of a 640 x 480 monitor. The Macintosh LC requires that pin 4 and 10 (SENSE0 and SENSE2) be connected to Ground to signal the connection of a 512 x 384 monitor (i.e., the Macintosh 12" RGB Display). The Macintosh LC requires that pin 10 (SENSE2) be connected to Ground to signal the connection of a VGA monitor. Pin 7 (SENSE1) is grounded in the Macintosh LC.
```  
The way those pins are interpreted depends on the Macintosh you're plugging the screen into, but the one we're interested in never seems to change much: `Grounding SENSE0 means the monitor is 640x480.`  
That's the resolution of the Performa Plus, so I'll be leaving the other two pins alone.  

# Time to connect

I grabbed a cheap DA-15 cable off AliExpress and made an atrocious Frankencable out of it:  
![end my life]({static}/images/performa/performa5.jpg)  

The connections mostly match what I wrote above, except some yellow/white cables magically appeared at the end that weren't in the video connector.  
I guessed those were probably only there for DA-15 compliance and led nowhere, so I left 'em unconnected.  

I hooked up the other end of the cable to a [freshly-salvaged](https://twitter.com/Difegue/status/1206696379483148289?s=20) Macintosh IIvx, powered everything on expecting to get a horribly mangled image and:  

![haha this is a disaste-wait what]({static}/images/performa/performa6.jpg)  
<sup><sub>Wow this actually works </sup></sub> I mean **of course it works!**  
![based]({static}/images/performa/izutsumi.gif)

# Screen size and final observations

![Macintosh IIvx]({static}/images/performa/performa7.jpg)  
The image quality is surprisingly good for a makeshift cable here -- No parasites or blurry picture.  
Although I found it odd that the image doesn't fill the screen entirely.  
Since the IIvx is a pretty old Mac(running System 7), I thought its video card might not have the horsepower to handle 640x480.  

No worries! Time to upgrade a bit and try the cable out on a Power Mac G3:  
![Power Mac G3]({static}/images/performa/performa8.jpg)  
This is **slightly** better! But not by much.  
The resolution utility in Mac OS 9 does say the screen resolution is at 640x480, so there are a few possible reasons:

* The CRT itself is configured to display the image like this  
* The screen actually supports resolutions higher than 640x480 and I fucked up forcing the resolution through `SENSE0`  
* Those white/yellow cables aren't there just for show pardner 🤠

For option 1 the only way out is aligning the CRT manually.  
While I'm less afraid of being zapped by CRTs after working on the eMac, this is next level and messing with factory settings is probably a terrible idea.

Option 2 can be tested on the Power Mac G3 by overriding the resolution with [SwitchRes2](https://www.madrau.com/SRXv3/html/SR2/indexSR2.html), which I'll try later.  
And if it's option 3, I probably won't even bother since the cable is already _pretty good™_ as it stands.  

![Can't believe I bothered that much just for a dumb Apple sticker]({static}/images/performa/performa9.jpg)  
I thank the gods of NASA in these festive times for the gift that is duct tape. Happy 2020!  
