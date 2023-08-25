Title: Introducing the McD's Sonic LCD Games Simulator
Date: 2022-04-13 00:00  
Category: Software  
Tags: sonic, mcdonalds, c#, avalonia, .net, lcd, game&watch, games, simulator
Slug: lcdonald
Authors: Difegue  
HeroImage: images/lcdonald/alpha1.jpg  
Summary: Yuji Naka: They probably eat McDonald's® hamburgers, I suppose? And I think they will get a complete line-up of Happy Meal® premiums. 

# 2022 Update

Check [here](./mcorigins.html) for the latest McOrigins-related post (and download links 🍟)

Or keep reading below to follow the... McOrigins Origin Story??? I'm going to be updating this again soon so there'll probably be a list of articles at that point

# 

Happy Sonic 2 Movie release day!... Is what I'd say if I'd actually managed to publish this on April 8th.  
It's been a while since Sonic's last been that present in popular culture, and I think I only fully realized that fact upon seeing the new [McDonald's toys](https://www.sonicstadium.org/2022/03/more-mcdonalds-sonic-2-happy-meal-toys-leaked/) planned for the movie.  

While ol' McD's and Sonic have had a [long](https://www.sonicstadium.org/2019/02/how-mcdonalds-couldnt-keep-up-with-the-worlds-fastest-hedgehog/) and [fruitful](https://www.sonicstadium.org/2006/01/uk-mcdonalds-sonic-x-happy-meal-promotion-begins/) [relationship](http://info.sonicretro.org/Yuji_Naka_interview_by_Sega.com_(June_14,_2003)), there hasn't been a line of Sonic toys released since I was a kid all hyped up for the then-upcoming Sonic X and the Shadow spinoff. <sub>Blissful years</sub>  

Thinking that a brand new generation of kids will fall prey to Hedgehog fandom makes me feel slightly older, but it mostly motivated me to take out my old collection of [Sonic McDonald's LCD games.](http://info.sonicretro.org/McDonald%27s_Sonic_LCD_games)  

![Have I made you proud, 12yo myself?]({static}/images/lcdonald/games.jpg)  

Those games were released in 2005/2006 and are both pretty well known... and kinda obscure!  
15 years later, the built-in batteries have started corroding (which isn't that big a deal considering they're quite far from the electronics), and I think most people won't get to experience those games.  

I've followed the [MAME LCD](http://blog.archive.org/2018/03/18/some-very-entertaining-plastic-emulated-at-the-archive/) game emulation efforts for a little while now, and entertained the project of doing something similar with those Sonic games.  
I don't have the skills or hardware to do "real" emulation ([processor decapping](http://seanriddle.com/decap.html) is a helluva thing), but I can certainly go as far as [simulation.](https://github.com/BdR76/lcdgame.js#simulation-vs-emulation)  

And y'know, better do what you can do, right? So I'm happy to release a first alpha for my Sonic LCD simulator.  
![Even when doing game stuff I can't help but make it look like a UWP app god damn]({static}/images/lcdonald/alpha1.jpg)  
## Grab it [here](https://github.com/Difegue/LCDonald/releases)!
(Windows only for now - I'll add Mac/Linux support later) 

I started out by simulating the (probably) most complex game of the collection, [Tails' Sky Adventure](http://info.sonicretro.org/Tails_Sky_Adventure).  
This _should_ ensure the simulator engine can handle all the other games, and well, haha Sonic 2 movie I guess! 
<sub><sup>Although you might argue Knuckles played a bigger role in the movie but eh w/e</sup></sub>

The simulator currently features dynamic view switching (so you can look at all those hires photos I took of the plastic things), and basic play/pause/stop controls. Keyboard only for now, although I'd like to add touch controls in the future.  

![It does look nice tho]({static}/images/lcdonald/alpha2.jpg)  

I'd ideally like to have most of the games simulated in a beta for [SAGE](https://twitter.com/SAGExpo/status/1513547421812363266?s=20&t=cxa2H5mMauV4-_UCdRy5NA)!  
We'll see how that goes.  

If you'd like to help out by digitizing some games(my scanner isn't the best) or even coding a simulator, you can keep reading for some tech details. 


# Very Quick Technical Breakdown

For the layout of the games themselves, I decided to use the same format as [MAME](https://docs.mamedev.org/techspecs/layout_files.html).  
That makes it so that editing layout doesn't require any coding -- And in the off-chance some crazy dude actually decaps the games for real in the future, hopefully this'll lay the groundwork for integrating them to MAME.  

```
<!-- tskyadventure.lay -->

<mamelayout version="2">

<!-- Define Elements -->

	<element name="manual_fr">
		<image file="tskyadventure_manual.jpg" />
	</element>
	<element name="front_open">
		<image file="tskyadventure_front_open.jpg" />
	</element>
	<element name="front_closed">
		<image file="tskyadventure_front_closed.jpg" />
	</element>
	<element name="back_open">
		<image file="tskyadventure_back_open.jpg" />
	</element>
	<element name="back_closed">
		<image file="tskyadventure_back_closed.jpg" />
	</element>
	<element name="game_bg">
		<image file="tskyadventure_bg.jpg" />
	</element>
	
<!-- Define Views -->
	
	<view name="Front Open">
		<screen index="0">
			<bounds x="1832" y="1313" width="300" height="380" />
		</screen>
		<element ref="front_open">
			<bounds x="0" y="0" width="3959" height="2639" />
		</element>
		<element ref="game_bg">
			<bounds x="1832" y="1313" width="300" height="380" />
		</element>
	</view>

	<view name="Front Closed">
		<element ref="front_closed">
			<bounds x="0" y="0" width="3959" height="2639" />
		</element>
	</view>

    [...]

</mamelayout>

```  

The simulator itself runs on good ol' .NET -- While I decided to use [Avalonia](http://avaloniaui.net/) for the front-facing app, the simulator core itself is separated [.NET Standard 2.1](https://christianfindlay.com/2020/12/21/net-standard/), and can run on anything .NET runs on.  

In case you think I'm bloody insane for using a Desktop app framework for games, nothing's stopping you from dunking the core into Unity and making your own frontend! That might be fun.  

Avalonia was interesting due to its easy SVG integration, which I considered critical for LCD game simulation.  
Once again copying what MAME does, the LCD layer is rendered as a SVG image, with specific groups toggled on and off depending on the game state.  

<img src="{static}/images/lcdonald/tskyadventure.svg"/>  
☝️ Also SVGs weigh nothing, which helps offset a bit the huge sizes of the photos/scans of the simulated games.  

In case you'd like to help, I've opened [tracking issues](https://github.com/Difegue/LCDonald/issues) for each game!  
While I do own most of them, I don't have the manuals for most, and some of the games have eluded me for over 12 years, like [Big's Fishing](http://info.sonicretro.org/Big%27s_Fishing).  
The issues go into detail as to what I own for each game, and what'd be needed to integrate it into the simulator.  

Thanks for reading!