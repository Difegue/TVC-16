Title: Replacing the PRAM Battery in a PowerBook G3 Wallstreet
Date: 2021-03-16 00:00  
Category: Hardware  
Tags: apple, mac, powerbook, repair, pram
Slug: wallstreet-pram-replacement
Authors: Difegue  
HeroImage: images/powerbook/powerbook_pram.jpg  
Summary: Ah yes, DMX's 2006 hit track, "Lord Give Me a Chime".

I got my hands on a [Powerbook G3](https://en.wikipedia.org/wiki/PowerBook_G3#PowerBook_G3_Series_(Wallstreet_Series_I)) recently. Lovely machine!  

![dingusbook screen]({static}/images/powerbook/powerbook_screen.jpg)  

But it had a few issues I quickly noticed once the machine booted without the [usual Mac chime.](https://www.youtube.com/watch?v=7G3SXTg7gDI) 

Mostly, **no sound**, and a screen with some flickering and purpleish artifacts.  
Kinda weak hinges too, but considering that those were apparently a [terrible mess](https://web.archive.org/web/20021003091053/http://www.ocf.berkeley.edu/%7Ekenao/unhinged/) during the service life of the laptop, I'm gonna consider myself lucky.  

Previous experiences with Macs have shown me that a missing chime usually happens when the PRAM(fancy apple name for CMOS) battery in the machine dies out.  
Replacing it usually goes a long way towards getting the computer back on track to healthy town.  

It probably wouldn't fix the sound missing in Mac OS, but since diagnosing that issue involves taking the laptop apart, we might as well replace the battery!  

## Building a replacement PRAM

Due to this being a laptop however, it doesn't use the [chonkster 3.6v](https://www.newertech.com/products/pram_3_6v.php) batteries you'd commonly find on other old Macs.  
Instead, after taking apart the entire machine (thanks [ifixit](https://www.ifixit.com/Guide/PowerBook+G3+Wallstreet+PRAM+Battery+Replacement/11?revisionid=HEAD)), you get to pull out a weird mini-rechargeable battery composed of 6 coin cells.  

![what in the goddamn]({static}/images/powerbook/powerbook_pram.jpg)  
(PSA: Some PowerBook models seem to only have [4 cells](https://www.mac-forums.com/threads/pram-battery-replacement-for-powerbook-g3-400mhz-lombard-alternatives.341150/) instead of 6.)

Luckily, those cells are Panasonic VL2330 3V rechargeable coin cells, and are still produced today!  
Although it does mean you need to basically re-build a PRAM set yourself.  

You'll see this for yourself upon opening up the set, but the cells are connected to each other on both ends matching the following schema:  

```
  ___    ___    ___      
 /   \  /   \  /   \    
|  - ---  - ---  -  |   --red wire 
 \___/  \___/  \_|_/
                 |
                 o--------white wire 
  ___    ___    _|_      
 /   \  /   \  / | \    
|  + ---  + ---  +  |   --black wire
 \___/  \___/  \___/               

  ___    ___    ___      
 /   \  /   \  /   \    
|  + ---  + ---  + -------red wire 
 \___/  \___/  \___/
                 
                 o--------white wire                
  ___    ___    ___      
 /   \  /   \  /   \    
|  - ---  - ---  - -------black wire
 \___/  \___/  \___/    

```
<sub><sup>Tried to throw this schema into [svgbob](https://github.com/ivanceras/svgbob) but it didn't look too hot so you'll have to deal with the OG ASCII</sub></sup>  
VL2330 cells are pretty cheap at your local [Chinese overlord](https://aliexpress.com/item/4001264470979.html), so you can build yourself a brand new PRAM for like $20.  

For assembly, I simply cut off the leads from the old PRAM and re-attached them to the new cells with ye ole' mates duct tape. 🩹 The stock PRAM is [spot welded](https://www.youtube.com/watch?v=GGTGIlT6JvM) together, so you can't simply unsolder the leads like you'd do with a dumb circuit board.  

## Results

Once the battery assembled, tested for continuity and put back in the laptop, did we get a chime on boot?  
Well, I did get a form of *noise* out of the laptop, but it sounded more like some radio screeching than an actual chime.  

Before putting the machine back together I had taken a look at the other pieces, and it's likely that the Sound/Power Board is dying and being what causes the remaining problems.  

![dingusbook power board]({static}/images/powerbook/powerbook_board.jpg)  

That [MLCC](https://en.wikipedia.org/wiki/Ceramic_capacitor#Multi-layer_ceramic_capacitors_(MLCC)) capacitor in front of the main power jack has certainly seen better days.  
<sub>It's always the fucking caps isn't it</sub>  

The screen still flickers, probably due to power draw issues coming from said board, but hey at least it doesn't artifact out anymore!  
