Title: That one time I wrote a memory patcher for an Android Emulator to keep playing FGO
Date: 2021-04-23 00:00  
Category: Software  
Tags: memu, android, patch, winforms, fgo
Slug: memu-patcher
Authors: Difegue  
HeroImage: images/memupatcher/about.png  
Summary: Why yes, I was the hacker known as 4chan this entire time!

I've been playing Fate/Grand Order for a pretty long time now, and have irredeemably fallen into [deep gambling addiction](https://twitter.com/Difegue/status/1289636218578378752).  
Besides the whole "paying for coomer JPEGs" thing, FGO often relies on heavy farming to get a bunch of resources.<sup><sub>Regular mobage trite really</sup></sub>  

![I haven't actually paid money for most of this it's just been already 5 years good lord save me type-moon release something else already]({static}/images/memupatcher/fgo.jpg)

While I do enjoy the gameplay to a point, repeating a battle 300 times is not fun no matter how you try to spin it.  
For a while, the easiest way to automate farming in FGO was to throw the game on an **Android emulator** and run a [Lua script](https://github.com/29988122/Fate-Grand-Order_Lua) on it.  
Alas, FGO is also quite known for its hate of **[any form of game/phone modification.](https://topjohnwu.medium.com/from-anime-game-to-android-system-security-vulnerability-9b955a182f20)**  
<sup>(I very much recommend reading this article if you haven't already done so, it'll be more interesting than anything written here.)</sup>  

At some point during the sweet summer of 2017, FGO stopped working on most famous emulator used to run it, [Memu](https://www.memuplay.com).  
The developers had implemented some extra checks for it when the game launches.  
Back then I was temporarily without a decent phone as well, so the incentive to get the bloody thing working again was quite high. <sup>Never underestimate what someone can do for his vidyagames and login streaks...</sup>  

Surprisingly, the checks were quite easy to circumvent, as they were only looking for **specific identifiers**, which could be replaced in the emulator's memory directly with a hex editor:  
<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2FDifegue%2FChaotic-Realm%2Fblob%2Fmaster%2FMemuPatcher%2FUnlimitedMemuWorks%2FForm1.cs%23L20-L24&style=github&showBorder=on&showLineNumbers=on&showFileMeta=on&showCopy=on"></script>  <sub><sup>Somehow doing a grand-scale string replacement in-memory like that didn't completely crash the thing, which is kinda impressive I guess?</sub></sup>  

I take no credit for figuring that one out, it came out of some [dudes on github](https://github.com/wDCat/ANRC/issues/98), who promptly decided to hide/delete it, thinking it'd make the trick last longer.  
![Imagine thinking that essentially performing brain surgery on a live emulator is a reliable and permanent fix]({static}/images/memupatcher/sikritclub.png)  
Oh, those _absolute, utter dinguses._  
![get a load of this freakin guy]({static}/images/memupatcher/lmao.gif)  
The method was obviously screenshotted and spread around on various boards.  
It worked, but busting out HxD everyime you wanted to run your farming script? 100% pain.  

The Github thread was starting to look like a mid-2000's warez forum with everyone begging for the method through Facebook by this point(seriously go flip through it it's unreal), which made me think things could be improved somewhat.  

So with the following goals in mind:  

* Destroying the secret club for the sole purpose of spreading chaos over the land  
* Making my own life easier so I could farm the upcoming Nerofest lottery in peace  

I wrote an automated memory patcher in .NET/WinForms in a few days:  
![I know there's a bunch of fucks but what can I say this was released anonymously]({static}/images/memupatcher/patcher.png)  
I say .NET, but this is almost more P/Invoke than interpreted considering all the patching code goes through Win32's `VirtualQueryEx/ReadProcessMemory/WriteProcessMemory` calls. ¯\\\_(ツ)_/¯  

Releasing this thing anonymously into the wild was especially funny, with various reactions such as:

* FUD about the patcher being malware despite being uploaded with the source code attached  
* Reddit tutorials being written referring to the program as the ["Patchouli Patcher"](https://www.reddit.com/r/grandorder/comments/6wi08i/episode_xiii_doom_or_be_doomed/dm89feh/) since I had [accidentally left my .vs folder in the uploaded code]({static}/images/memupatcher/suofile.png) like an idiot
* FUD about the patcher [getting your FGO account potentially banned](https://pastebin.com/U7qb6Jbh)  
* People begging for support screaming that they did buy Sonic Mania (sega should pay me for all this free advertising I gave them)

I never got it to reliably work on Windows 7/8, but nonetheless it seemed to be quite popular! (Looking back at the source, I suspect there's something wrong with my usage of `SYSTEM_INFO`.)  
Most importantly, it spread the method around so other people could implement it in Cheat Engine or similar.  

## Closing thoughts

As a result, I got my share of anonymous hacker fame, saved some login streaks (including the guy [making the Lua farming script](https://github.com/wDCat/ANRC/issues/110) so yknow, what goes around comes around ✨), and autofarmed to my hearts' content until [Nox](https://www.bignox.com/) got reliable FGO support, at which point I switched and never looked back. 👏  

I've uploaded the latest version of the code I had here: [https://github.com/Difegue/Chaotic-Realm/tree/master/MemuPatcher](https://github.com/Difegue/Chaotic-Realm/tree/master/MemuPatcher)  
I don't think this will be useful to anyone considering it's just a half-baked memory scanner and Cheat Engine literally does the same thing, but you might get a laugh out of it.  

I think FGO still manages to block emulators every now and then, but I've entirely moved to just running [FGA](https://github.com/Fate-Grand-Automata/FGA) on my phone instead of the Lua script these days, so I don't really care anymore.  
