Title: LRR goes neumorphism (well, the icon at least)
Date: 2021-03-19 00:00  
Category: LANraragi  
Tags: lanraragi, icon, design, neumorphism
Slug: lrr-icon-study
Authors: Difegue  
HeroImage: images/lrr_nuicon/opengraph.jpg  
Summary: haha gloss and shadows go brrrrrrrrrrrrrr

![old logo and favicon]({static}/images/lrr-nuicon/old.png)  

The favicon you've probably already seen a thousand times if you have a [LANraragi](https://github.com/Difegue/LANraragi) install was ripped off from a Japanese Monogatari website sometime in late 2014. (get it b/c it's araragi and you see the ahoge and everything haha)  
The logo came a bit later(late 2016), but it's essentially just an edit of the ubiquitous [fa-cubes](https://fontawesome.com/icons/cubes?style=solid).  

The favicon served me well enough, but it's starting to feel really low-res, and doesn't really work well on dark backgrounds.  
As for the logo, it doesn't look very nice at low resolutions either if I were to make it the new favicon.  

Therefore, I've been wanting to update the LRR logo in order to make it:  

- Legible/Recognizable enough at low resolution
- Work on both light and dark backgrounds
- Not a ripoff of existing art (don't want to risk a lawsuit from aniplex and fontawesome if i ever make it big i swear on me mum they'd do it we live in a society)

while not losing what makes it **unique**, by which I mean keeping the ahoge motif.  

<img width="300" alt="can you believe this image is 9 years old already oh my god where does the time go" src="/images/lrr-nuicon/rrg.jpg"/>  

## Thoughts and process

[Neumorphism](https://www.justinmind.com/blog/neumorphism-ui/) is the new design meme, but outside of outlandish dribble mockups it seems to just translate to softer shadows and more transparency, with a little bit of 3D thrown in.  
<sup><sub>Not a design expert please don't scream at me for not getting it</sup></sub>

So, let's make a 3D icon! Using the one and only free 3D tool all grand designers use, <s>Blender</s> Paint 3D by Microsoft:  

![it aint stupid if it works]({static}/images/lrr-nuicon/p3D.jpg)  

I took the existing 3D logo I'd already made for the [5 years hacktoberfest](./hacktoberfest-lrr-2.html), and started iterating from there.

To help with recognizing the icon at low-res, the best thing to do was to bring in some **color** to the blocks.  
The color scheme was inspired by the WinRAR icon, since LRR deals with archive/compressed files basically all the time!  

![the finger tool in gimp has been my best ally for over 8 years now and it aint stopping anytime soon]({static}/images/lrr-nuicon/study.jpg)

Fully coloring them looked kinda garbo, so I went **arthouse** and just scribbled some lines.  
Paint 3D did a surprisingly good job at handling the breadth of the lines depending on the depth, and it reminds me of the NeXTSTEP blocks so I like it:  

![damn its like i'm steve jobs]({static}/images/lrr-nuicon/OIP.jpg)  

I was kinda scared of the 3D ahoge looking like a piece of poop straight outta [Duke Nukem Forever](https://www.youtube.com/watch?v=Lk2hzFC5Zok) with the glossy lighting and low polycount, but thankfully it looks quite good after some post-processing in <s>Photoshop</s> GIMP to smooth it out.  

<img alt="new favicon" src="/images/lrr-nuicon/new.png" width="550"/> <img alt="hmu in the comments if you actually read those alt texts" src="/images/lrr-nuicon/splash.jpg" width="250"/>  

I really dig the way it's positioned though! It pops out **way** more than in the previous icon, and having it rotated to the side brings a lot of extra depth.  
Having it burrowed a bit more into the blocks also makes it recognizable even at low resolutions. <sup><sub>and it kinda looks like a parasitic slug so that's cool </sup></sub>  

The design doesn't fare as well as I'd hoped on dark backgrounds however, so I slapped a squircle straight out of the Apple playbook for the icon variant.  
It looks a bit weird on Windows since squircles aren't really a thing in MS iconography, but the Windows app is just a launcher anyways so eh ¯\\\_(ツ)_/¯  

## Closing thoughts

_m8 this icon thing is easy who needs designers rite just slap some 3D blocks and ur good_  

I wanted to name 0.7.7 Video Crime at first since it's basically the only Tin Machine song I like, but since I pick the Bowie song names proportional to the quality of the release, and 0.7.7 was **super** huge, I went for Pallas Athena instead.  
Probably my favorite song from _Black Tie White Noise_, although I love most of the album it's real darn good  

I took the opportunity to remake my OpenGraph Github splash as well, using Inter as the typography:  
![now in the iOS app store! what have I become good lord forgive me for I have sinned]({static}/images/lrr-nuicon/opengraph.jpg)  
I'll kinda miss the low-res GIMP pepper from the previous version.  
