Title: Some notes on restoring a 2003 1GHz eMac 
Date: 2019-11-28 00:00  
Update: 2019-12-19 00:00  
Category: Hardware  
Tags: apple, macos, emac, lcd, mod, diy
Slug: emac-lcd-mod
Authors: Difegue  
HeroImage: images/emac/emac_end.jpg
Summary: I guess this is an Apple blog now.

I recently found an old [eMac](https://en.wikipedia.org/wiki/EMac).  

![yeah rip]({static}/images/emac/emac (1).jpg)  

It was not in good shape.  
I never really dabbled in Apple hardware before this (in fact my first real hands-on with Mac OS as a whole was what, 8 months ago ?), so I quickly tried booting it and it seemed to work! Except the CRT coil was glowing red. Neat.  

There's a surprising amount of documentation online about restoring eMacs -- Probably due to a mix of the failing analog boards and the low pricepoint of the machine. As a result, I tried fixing the thing. Here are a few notes.  

## Getting some reading done

The essential reference for eMac modification is [Leo Bodnar's site](https://web.archive.org/web/20180220163441/http://www.lbodnar.dsl.pipex.com/eServer/), or at least the archive.org snapshots of it, as it has since then died a brutal death.  

Other helpful links were [iFixit](https://fr.ifixit.com/Device/eMac) for figuring out how to dismantle the beast, and the [Original Apple service manual.](http://gmcotton.com/Ham_Radio/MISC%20Manuals/Mac/emac%20service%20manual.pdf) Basic stuff.  

My initial reference and guide for most of the process was this [2006 article](https://ierna.com/2006/07/02/emac-lcd-conversion/) on an eMac LCD conversion. Quite detailed but it misses a few details, which I'll go over here.  

## Connecting the logic board to a working screen and power supply

Once the machine taken apart, I've recovered the original power and video cables that were connected to the CRT board, and modified them to connect to Molex/VGA respectively.  
The pinouts can be found on the [Leo Bodnar archive](https://web.archive.org/web/20180220163441/http://www.lbodnar.dsl.pipex.com/eServer/), alongside a more detailed breakout of the different boards present in the machine.

As far as the power cable goes, it can really connect to anything that outputs both 12 and 5V -- As mentioned in the archive, the eMac actually expects 20 and 19V on a few of its pins for Firewire support, but using 12V for those works fine enough.  

I did redirect the hard drive and DVD player to run off the PSU directly instead of the eMac's integrated down-converter board, in order to make sure those have the voltage they need.  

![damn that's a lot of icons]({static}/images/emac/emac (2).jpg)  

Well whaddaya know, this actually works. Time to drop all this good stuff into a case.  

## Dropping the LCD screen

Any well-proportioned 17" LCD fits the eMac front panel, but if you're like me and blindly followed the ierna blog thinking you could just slam it in and call it a day, you'll probably be surprised.  

![lcd dropped in emac front panel]({static}/images/emac/emac (3).jpg)  

My screen had bigger bezels than the one he used, which required me to cut off the microphone support stand and use tape to fix it instead.  
![microphone support(pic from ierna)]({static}/images/emac/micro.jpg)  
(pic from ierna, as I didn't take a picture of this part.)  

This made the screen fit fine in the panel, but the CRT cowl which comes on top of it was too small as well!  
The cowl is essential to the structure of the machine, but luckily you can get away with just cutting the corners.  
![damn that's a lot of icons]({static}/images/emac/emac (4).jpg)  

As a tradeoff though, I didn't cut the outside of the case like ierna, so all those modifications are invisible.  
Sure, I can't turn off the screen and the OSX Menu is slightly hidden by the front panel but ehh, I'll fix it in software.  

## Mounting the power supply

Mounting a full-sized ATX PSU in the original case was challenging, and is frankly overkill considering the eMac doesn't draw that much power.  
Sadly it's all I had on hand so I rolled with it.  

There are mounting holes on the plate since it originally housed the analog board, but of course they don't line up whatsoever with ATX, so I had to make some custom mounting brackets to get it to stay fixed. I really hope you guys don't do this.  

![screwing those bottom screws with the plastic parts blocking your paths was a real joy]({static}/images/emac/emac (5).jpg)  

One last hurdle caused by the ATX supply was that it was blocking the pins of the plastic case when putting the eMac back together.  
The pins go in the two large holes on top you can see there, so I had to sand them down a bit to make them smaller.  

And it's done! Well, almost.  

## Display refresh rate hell

![pictures taken moments before disaster]({static}/images/emac/emac (6).jpg)  

So, I got 10.14 Tiger booted up, listened to some music through iTunes and it seems fine!  
Then I went to toy a bit in the settings and everything fell apart.  

As mentioned by lbodnard, the eMac's screen resolutions use **very high** refresh rates (up to 100Hz), which go far beyond what old TFT LCDs can handle.  
OSX seemed to know about this at first and set a 75Hz rate so my LCD was usable, but a misstep on my part in System Settings set the resolution to an unusable rate.  

Therefore, my eMac is left without a screen again. 😐  
Resetting the resolution settings [seems rather easy](http://hints.macworld.com/article.php?story=2001100114532165) if you have filesystem access, but I don't, so I'll probably have to take the machine apart again and plug in a newer screen that can handle the high rates.  

If there's one warning to take from this, it's that you should probably enable Mac OS's built-in SSH/VNC servers so you can run the eMac headless -- Screen lockout happens easily!  

## Update: Getting out of display rate hell

The solution to the above conundrum was indeed plugging in another screen. Luckily OSX wasn't stuck at some super high rate, so a more recent LCD did the trick.  

![all's right with the world thanks to switchresx]({static}/images/emac/emac_end.jpg)  

I promptly installed an old version of [SwitchResX](http://www.madrau.com/index.html) in order to disable all the extra resolutions the eMac adds to account for its normal CRT screen.  
This means no more surprises when starting a game that goes to fullscreen and tries to guess the best resolution out of what the machine offers.  

And I guess I'm finally done with this machine! It took quite a while.  
<sub><sup>The hard drive is starting to fail though so I'll probably need to clone it and drop a new IDE drive in this sucker...</sup></sub>

## Final notes  

My first experience with OSX was with 10.14 Mojave a few months back -- Using 10.4 Tiger on this machine, it's pretty funny how 98% of the UI has essentially stayed the same in 13 years.  
Guess I'm too used to Windows switching everything around every couple of releases.  

At least I don't have to learn how to use the Finder again!  
