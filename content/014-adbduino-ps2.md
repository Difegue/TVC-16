Title: Using PS/2 keyboard/mice on old Macs with Arduino
Date: 2020-02-12 00:00  
Category: Hardware  
Tags: apple, macintosh, mac, arduino, adb, ps/2, diy, retrocomputing
Slug: adbuino-ps2
Authors: Difegue  
HeroImage: images/adb/adbduino-final.jpg
Summary: It's time to deal with ADB. Not the Android one!

My Mac fleet has been progressing nicely with all the [previous](https://tvc-16.science/emac-lcd-mod.html) [restorations](https://tvc-16.science/performa-plus-display.html), but I still didn't have a way to control the pre-OSX machines. Those machines came to me keyboardless, and I initially thought it'd be no problem at all!  
Alas, I did not know about the terrifying Apple Desktop Bus.  
![noooooooo]({static}/images/adb/pinout.jpg)  
[ADB for short](https://en.wikipedia.org/wiki/Apple_Desktop_Bus), this connector was used to plug keyboards, mice, joysticks and what have you into Macintoshes until USB took over.  Since I won't be able to use my old PS/2 stuff, might as well invest into some ADB devic--
![the apple tax is fucking real]({static}/images/adb/ebay.jpg)  

## 😥 😥 😥 
I shouldn't be surprised really, but I feel bad shelling out 40€ for a yellowed keyboard/mouse combo when I already have tons of PC ones laying around.  

# A quick tour of ADB replacement solutions

There aren't many solutions to convert other devices to ADB on the market.  
The best one seems to be the [USB-ADB Wombat](https://www.bigmessowires.com/usb-wombat), but that doesn't exactly come cheap either!  
Although it basically offers the full shebang and works with more modern USB keyboards.  
![wombat]({static}/images/adb/wombat.jpg)  
You also have [this thing](http://www.geethree.com/adb/), which _a contrario_ is rather old and only works for mice. Meh.  

Turning to DIY solutions, most of the stuff out there is meant to use ADB keyboards on modern machines, using code from [TMK](https://github.com/tmk/tmk_keyboard/tree/master/converter/adb_usb). People really love their Apple Extended Keyboards!  
Which is nice and all, but the opposite of what I need.  

After a bit more searching I did end up finding [this spare forum post.](http://thinkclassic.org/viewtopic.php?id=630)  
PS/2 to ADB, both keyboard and mouse running off an off-the-shelf Arduino? Sounds great!  

The code is available [on bbraun's SVN](http://synack.net/svn/adbduino/), so I grabbed an Arduino off my dead project pile and got to work.

# Making the adbduino adapter

The provided .osm file for the circuit board needs [Osmond](https://www.osmondpcb.com/ ) to be opened.  
Opening it, it's all pretty simple however, no need for extra resistors or anything:  

![adbduino circuit board]({static}/images/adb/osmond.png)  
The PCB has spots for two ADB connectors, but the second one is really just meant to enable passthrough to other ADB devices if you have any.  
Since I wasn't sure this stuff would actually still work, I breadboarded an abomination with just one connector.  
![end my life]({static}/images/adb/adapter.jpg)  

The original project used a Pro Mini, but the Nano I had on hand is essentially the same thing, so no problem on that front.  

Hooked it up to the ol' IIvx, and heck, it works! With some caveats.  

# Using n' troubleshooting

My first major issue came with the mouse I was using -- It was struggling to synchronize itself with the ADB bus, essentially wrecking havoc on the Mac with random movements and clicks when moved.  
![end my life]({static}/images/adb/adbduino-early.jpg)  
When eventually synced however(which could be helped by arcane methods such as <sup><sub> flipping the mouse over and repeatedly pressing caps lock</sup></sub>), it ran fine.  

Thankfully, just switching out the mouse for an old USB model with a USB->PS/2 adapter fixed everything.  
I don't recommend buying new PS/2 mice from AliExpress if you really need them!  

The other big issue I had came from the keyboard skipping keys and occasionally staying "stuck" on the last keypress, resulting in a text a bit like `thissssssssss`.  
Some debugging with the Serial monitor later, there were essentially three potential cases going on when releasing a key:  

```
A) 0x3C (key pressed) -> 0x3D (key released)  
B) 0x3C (key pressed) -> 0xFF (keyboard error)  
C) 0x3C (key pressed) -> 0xFF (keyboard error) -> 0x3C (key pressed)
```  

Case A is the normal one, B skipped the key, and C was causing the stuck key problem.  
This is **totally** the keyboard's fault (heck, I've had this one since Windows 98), but since this solution is about being as cheap as I can possibly be, I'd rather try to fix this through software. _aww yeah it's arduino hacking time_  

<iframe width="516" height="290" src="https://www.youtube.com/embed/1ZsETdpmvR0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

...Well that's what I'd like to say, but I'm far from being good at hardware programming and dropped my bitwise operators, so I only managed a half-fix.  

* By [storing the last pressed keycode](https://github.com/Difegue/Chaotic-Realm/blob/8c8afceb654f921774d88ac99e36613b679c1b9f/adbduino/sketch/adbuino.ino#L313), we can recalculate its keyup variant and send that to ADB instead when we encounter a `0xFF` error code. This fixes case B!  
* Case C is fixed by adding a [timer check](https://github.com/Difegue/Chaotic-Realm/blob/8c8afceb654f921774d88ac99e36613b679c1b9f/adbduino/sketch/adbuino.ino#L455) so that a further keypress is dropped if it comes too soon for human hands.  

Adding timers is pretty sloppy and nearly breaks the ADB implementation since the protocol is super dependent on timing, but commenting out all the `Serial.print` debug calls makes it fast enough to pass! <sup><sub> damn I'm good at programming</sup></sub>

Although just dropping this bugged keypress fucks with the keyboard's internal state, so the next time said key is pressed for real, it'll be **skipped**.  
This could be solved by sending some extra stuff on the PS/2 side of things but ehhhhhh, good enough. This is much less annoying for casual use than the stuck keys.  

# Spare thoughts

![I retrobright'd this powermac and it looks pretty darn good now]({static}/images/adb/adbduino-final.jpg)  

Building this thing cost me around **5€** to get an ADB cable, some PS/2 connectors and the PS/2 mouse, which eventually proved itself to be useless.  
If you don't own spare PS/2 devices or an Arduino from a dead project, the total cost probably rises to 10€ or so.  
The ADB connector itself was salvaged from an old destroyed PowerBook dock, but any female S-video connector will do, as they both use DIN-4.  

All around, this is much cheaper than buying a real ADB keyboard or a USB adapter! Although it certainly isn't flawless.  
The issues I had seem more related to my PS/2 hardware being old than the adapter itself, however.  

You can find my hacked-up version of the adbduino sketch [here](https://github.com/Difegue/Chaotic-Realm/tree/master/adbduino).  
