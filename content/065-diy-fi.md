Title: Making new microgames in WarioWare DIY, 14 years later
Date: 2025-01-28 00:00
Category: Gamedev
Tags: nintendo, wii, nintendo ds, warioware, doujinsoft, mio, diy, gamedev
Slug: diy-fi
Authors: Difegue
HeroImage: images/doujinsoft/x68k-2025.png
BskyPost: at://difegue.tvc-16.science/app.bsky.feed.post/3lgwb45tawk2o
Summary: hahaha!!! i made a fake OS on the nintendo ds!!!

Despite running the largest [WarioWare DIY archive](https://diy.tvc-16.science/) for about eight years now<sup id="ref-1">[*](#note-1)</sup>, I hadn't made any games with it since... [wow, 2011!](https://diy.tvc-16.science/games?id=66ff7257b3d7ea3361c3745ed36ed05e)  
DIY is of course very limiting as a game creation tool, but I'm quite grateful to it for being the one of the ways I released "proper" games online, after multiple attempts with Game Maker 7/8 in the late 2000s<sup id="ref-2">[**](#note-2)</sup>.   

While running those old GM games on modern hardware is a pain, the various efforts around DIY have made it surpisingly easy to pick up and use even nowadays. <sub>(I don't think you'd be getting [skibidi games](https://diy.tvc-16.science/games?id=2d92ffcc9d1ec20a024d37210a35f51d) otherwise..)</sub>  
There's the [built-in](./doujinsoft-3.html) players on DoujinSoft, of course, but also working online with [WiiLink](https://www.wiilink24.com/) and Wimmfi for the original games.  

..And the new kid on the block, [DIY-Fi](https://diy-fi.net/)!  
This new service fully reimplements DIY's online store for the DS version of the game, bringing back weekly games<sup id="ref-3">[***](#note-3)</sup> to download, alongside design contests.  
![DIY-Fi showing 2025 Halloween contest winners on real hardware](./images/doujinsoft/diy-fi.jpg)  
A design contest popped up for Halloween, so I thought, why not test myself a bit and see if I _could make a game without redoing any of the tutorials 14 years later_?  
<sub>(DoujinSoft now supports `iframe` embeds! Feel free to embed all your DIY microgames and comics on your own websites.)</sub>  

<iframe src="https://diy.tvc-16.science/games?id=a7f667db4362842bee783123cd235699#iframe" width="536" height="490"></iframe>  
...OK, it was still pretty easy. The _Game MakerMatic_ creation tool within WarioWare DIY isn't massively complex!  

Due to having maintained DoujinSoft for all those years, I never really forgot all the concepts and terminology, so I guess I had a bit of an advantage.  
I think the only thing I had to look back up after all this time was how to do randomness?  

# A review of the MakerMatic in 2025  
 
How does it stack up as a game-making tool though? I think it's alright!  
You're very constrained, obviously, but that also makes scope creep essentially **impossible**, which is very nice if all you want to do is bang out a thing in a few days hunched over your Nintendo DS and call it a day.  

The palette is a bit low around 32 or so colors, so you end up relying on dithering pretty fast.  
While you might think the most limiting think in the MakerMatic is the "point" system that dictates how much pixel art you can cram into the 64 kilobytes of an individual microgame, I think the true thing that kneecaps you is the maximum of **6 AI statements** per object.  

In DIY, AI is not a capitalist buzzword for poorly functioning chatbots, but is essentially the equivalent of a `if/else` function in normal programming. So broadly speaking, you only have 6 `ifs` per object.  

You can imagine this gets limiting very fast! Combined with the fact each object can only hold **one** boolean variable, any form of complex logic usually ends up eating through your entire _15 object_ limit.  
![A bunch of objects in Doujin-x68k, entirely filling out the point limit!](./images/doujinsoft/diy-objects.jpg)  
Now there are some tricks you can employ to maximize your object use -- Offscreen positions can be used as makeshift additional integer variables, you can also rely on the animation system, etc.. But it kinda all comes back to the fact **logic is the biggest limiter**.  

Not allowing the use of the NDS buttons or microphone is also a bit of a missed opportunity - I can understand the mic if you wanted to keep interoperability with the Wii version<sup id="ref-4">[#](#note-4)</sup>, but the D-pad and A/B buttons would've been a great way to mix things up without adding much complexity. 

There's also no real random function in DIY - The game itself teaches you to make use of one of its built-in "random placement" functions to act as your RNG by then doing a position check. It's clever! But also kind of hacky!!   

# What about... second game??? 

After _SpookOS_, I wanted to actually test those limits and see how much functionality you can cram in a WWDIY microgame.  

There are some pretty impressive DIY creations out there that do [Anaglyph 3D](https://diy.tvc-16.science/games?id=e3c8d428afe0c193710bb0258874e7f2) or [multi-room puzzles](https://diy.tvc-16.science/games?id=e44be2dc1cc27af1de4096c28189290c), but I wanted to try my hand at making a game that just crams a bunch of various stuff in.  
We're going **maximalist** baby! It's the [Ring Racers](https://www.kartkrew.org/) of WarioWare DIY!  

There [are](https://diy.tvc-16.science/games?id=88ba7dd23152109b8712f4a209dd26ef) [a](https://diy.tvc-16.science/games?id=0f14d0ddc0e6def0b45adbdbb16ccc6f) [lot](https://diy.tvc-16.science/games?id=3d7c9d2797d3ce65c3a2dd84ea70d278) [of](https://diy.tvc-16.science/games?id=7a1adf1d1e31185bddf1904d59186e00) [DIY microgames](https://diy.tvc-16.science/games?id=f31e0eb5beefc9336826f92d6a77287b) that replicate Windows or computer interfaces already... But most of these are pretty simple, and I love my toy operating systems!  

So I grabbed the boss template and made a tiny fake OS using graphics from [Funtography](./funtography.html), with multiple windows and embedded games/messages.  
I'd just traced the graphics as usual for SpookOS, but here I caved in and used [mioedit](https://www.romhacking.net/utilities/1011/) to import some bitmaps from the computer. This approach isn't perfect due to the palette limitations though, so I still had to do some redrawing.  

<iframe src="https://diy.tvc-16.science/games?id=2124d89e60265d2535101bc58f7a22fb#iframe" width="536" height="490"></iframe>  

Of course there's realistically not _that_ much you can do in DIY...  
But I had fun figuring out the balancing act between the various point, AI, and object limits.  

To make an object blink, you _can_ use a sprite animation... Or you could just rely on two variables to teleport it out of bounds and back in within the same AI statement. Stuff like that. 

I was pretty happy with the microgame, so I forcefully sent it to 150 Wii consoles through WiiLink with the yearly DoujinSoft newsletter.  
That's the harsh truth of marketing, baby...  
![And I get to make a Songs of Innocence joke! phenomenal](./images/doujinsoft/wiimb-u2.jpg)  
I do think there's a bit of a framework here for "zine-like" DIY games, that contain just tiny little bits of text, graphics and maybe showcasing some tricks you can do with the MakerMatic.  
Putting together text in the editor on the NDS is **maximum pain** though, so I don't think that'll happen!  
#

<sup id="note-1">[\*](#ref-1) DoujinSoft has now been running for a longer time that the official Nintendo WFC service did for DIY on Nintendo DS... Also I was rewatching some older Game Center CX episodes and Arino was only 32 at the start of the show?? holy shit</sup>  
<sup id="note-2">[\*\*](#ref-2) **Before** it got bought over by yoyo games! can you imagine? I was too young to get into Klik & Play/Multimedia Fusion when it was the [hype gamemaking tool for kids](https://jtholen.bandcamp.com/album/new-active-object). </sup>  
<sup id="note-3">[\*\*\*](#ref-3) The weekly games are powered by snapshots of the latest additions to the DoujinSoft dataset! It's really cool to see the archive being used in that way.</sup>   
<sup id="note-4">[#](#ref-4) Although they **could** have used waggle/motion controls on the Wii in place of the mic! It'd have been silly but pretty fun if you ask me.</sup>  