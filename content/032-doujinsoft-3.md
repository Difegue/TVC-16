Title: DoujinSoft is 5 years old -- v3.5 is now live!
Date: 2022-10-06 00:00
Category: Software
Tags: nintendo, wii, wiiconnect24, riiconnect24, warioware, doujinsoft, mio
Slug: doujinsoft-3
Authors: Difegue
HeroImage: images/doujinsoft/diy-hero.jpg
Summary: Freeing DIY from the shackles of Nintendo hardware...almost.

[The DoujinSoft Store](https://diy.tvc-16.science/) is 5 already! It still stands as the last thing I [wrote in Java](/doujinsoft-2.html) and I wasn't expecting it to hold that long ¯\\\_(ツ)_/¯  

It still receives new content fairly often - Thanks to everyone who contributes!  
To celebrate the occasion <sup>(not really it's just lining up nicely)</sup>, the store has been given a fresh coat of paint... alongside some new mysterious buttons?  

![what could this play button possibly do?](/images/doujinsoft/playbtn.jpg)  

# The mystery button

DoujinSoft has been able to _play music_ and _read comics_ in the browser since it was released, but the biggest part of WarioWare DIY's user-generated content has always been absent from the browser...until now.  

![not gonna lie I was pretty good at tracing pixel art back then](/images/doujinsoft/gamepreview.jpg)  
If you told me 12 years ago I'd still be looking at my microgames but on a 4K display through the Internet, I probably wouldn't have believed you.  
## Available **now**, the DoujinSoft store now allows you to play _every single WarioWare DIY game in your browser._  

This is something I was secretly hoping for ever since launching the service, but I wasn't really expecting anyone to actually go and reverse-engineer DIY AI to make it happen.  
95% of the work that went into this update comes from **[yeahross'](https://yeahross.itch.io/)** exceptional Mio-Micro project, which has been cooking for a few months already. You should certainly go throw some flowers his way!  

# Player integration

I'd have felt kinda bad just pushing out this update and writing a blogpost about it without contributing _something_, so by leveraging the mio-micro player, there's a fun little bonus in DoujinSoft's **collections** pages now:  

<video controls repeat autoplay muted src="images/doujinsoft/player_demo.mp4"></video>  

Huh, it's _almost_ like a real WarioWare game now!  
The animations are taken straight from [Animate.css](https://animate.style/) which isn't really designed for that sort of thing, but it's unreal how well it works.  
The sounds are a bit of a [deep cut](https://www.youtube.com/watch?v=40GhbBZGYZY), but if like me you've been listening to the DIY jingles for years, a bit of change is nice. 😩  

Some caveats in this first version:  

- There is no speed-up mechanic, but considering how obtuse some of the games are to win, I wonder if you'll really need it 🙃 
- Boss games **are** included and will give you 1-UPs, but they'll come in just as randomly as normal games do.
- While mio-micro is **very** good at simulating DIY games, there might still be some emulation errors that make some games unwinnable. Please let us know on the [mio-micro Github page!](https://github.com/yeahross0/Mio-Micro)    

# Some other stuff

In yet [another](/mcorigins.html) Spline [frenzy](/stylophone-25.html), the store now has some new backgrounds and promo art!  

![haha truck goes brrrrrrrr](/images/doujinsoft/diy-hero.jpg)

After 5 years without it, DoujinSoft now also has proper _blurred previews_ for NSFW content.  
You can disable those if you want. <sub><sup>And yes you can play them in the web player</sup></sub>  
Flagging NSFW content in the database is an ongoing work, so if you find some unblurred stuff make sure to let me know!  

The collection minigame player is limited to the prebuild collections for now, but I hope to _eventually_ add a feature to allow people to craft their own collections/playlists and share them via QR codes or similar.  
Maybe I'll put up a _Halloween microgame playlist_ for people to enjoy? Let me know if you have any spooky games you like. 

**[Hacktoberfest](https://hacktoberfest.com/) has just started**, so if you want to contribute to the DoujinSoft experience **yourself**, I'll gladly accept any help, and you can get a shirt out of it! <sub><sup>Please!</sub></sup>  

Apart from that uhhhh  
### Some General system stability improvements have been made to enhance the user's experience.  

[Please enjoy!](https://diy.tvc-16.science/)  
