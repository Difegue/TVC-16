Title: Migrating a game collection database from CLZ Games to Gameye 
Date: 2025-09-27 00:00
Category: Physicality of Gaming
Tags: video games, collection, migration, clz, gameye, sqlite, powershell, scraping, subscription hell
Slug: clz-to-gameye
Authors: Difegue
HeroImage: images/games/collection.jpg
BskyPost: at://difegue.tvc-16.science/app.bsky.feed.post/3lugupqum4c2z
Summary: ONE MORE SUBSCRIPTION REJECTED 

I own a relatively mid-sized [game collection](/kallax-crt.html), and it has recently gotten to the point I unfortunately can't always precisely remember everything I own when I'm hunting through garage sales.  
<sub>Mostly because I've gotten into 360/ps3 more where big AAA series became more of a thing and no I can't fucking remember if I already bought uncharted 2 or 3 or asscreed 2 or 4</sub>  

So I got into logging all the stuff I own...  
And I would've run out of motivation _really fast_ if I had to manually type in every game name!  
I searched a bit and ended up using [CLZ Games](https://clz.com/games), which has a **fantastic** barcode scanner I threw my entire collection at like it was clearance on [Aisle 10](https://www.youtube.com/watch?v=wzM0t96x84A).  
![most of my collection logged onto CLZ](./images/games/clz.png)  
I have to give a lot of props to the app overall - Their database is great and differentiates between collectors, platinum/players choice editions, and the barcode scanner found every single game I scanned through it, regardless of region.  

The UI is also quite nice and there's a web version... I'd happily use this!  
**Except it's subscription-based.**  
![its a fucking subscription again god damn it](./images/1-2-hurts-just-a-little-bit.jpg)  
Luckily the app has an **export function**<sup id="ref-1">[*](#note-1)</sup>, which means with a little bit of scripting, I can get my scanned collection out and into something else that won't cost me 20€ a year<sup id="ref-2">[**](#note-2)</sup> to look at.  

# The competition  

Since the point is to have the collection on the go for cross-checking, I wanted to have it on **Android**.  
I could technically just have everything in a spreadsheet and use Excel on the go or something, but being able to filter by console and easily keep track of whether I own the box/manual for a given game are very nice to have.  

It also needs to have an **import function** of its own so I can pipe the data into it.  
So! As the title of the blogpost spoils, I ended up choosing [GAMEYE](https://www.gameye.app/) as the host for the export.  

I originally looked at Gameye for initially scanning my collection since it also has a barcode scanner... But their database is much worse than CLZ on that front and I was having a pretty low success rate<sup id="ref-3">[***](#note-3)</sup>.  

# The export/import formats 

CLZ Cloud's exports are pretty straightforward: You can either get an XML with all the info, or a custom CSV/TXT with fields of your choosing.  

For the rest of this blogpost, I went with a CSV that has the following columns:  
```
Title,Platform,Region,Box,Manual
"ChuChu Rocket!",Dreamcast,Europe,No,No
"Crazy Taxi",Dreamcast,Europe,Yes,No
"Crazy Taxi",Dreamcast,Japan,Yes,Yes
"Crazy Taxi 2",Dreamcast,Japan,Yes,Yes
```

Gameye's import/export functions are a bit less easy to work with, but relatively straightforward.  
Exporting your database from the app gives you a **.ged file**, which is just a zipped SQLite database.  

![good ol' DB explorer for SQLite showing a Gameye database]()  

# The script  

I hate SQL about as much as I hate subscriptions, so I decided to just do csv-to-csv conversion, using DB Browser after the fact to actually insert the data in the Gameye DB.  

The meat of the complexity here is to find the Gameye IDs for each game, since the other columns map relatively easily to the other info we have.  

Luckily, Gameye has a freely available online [search tool](https://www.gameye.app/encyclopedia)! And all of the IDs match what the mobile app uses, which means we will perform the heretical act of... **web automation.**  

Since we need csv processing and web requests, I wound up using Powershell for the scripting, since it comes with both of those things out of the box. 



All that's left is to write this csv into the DB, zip it up again, import into the Android app... And presto!  

# Closing words
![The collection, side-by-side in both CLZ and Gameye. Shoutout Surface Duo my beloved](./images/games/collection.jpg)  

The script is very much a quickly hacked thing and the search could certainly be improved, but out of 450 items I ended up with like 30 false positives and 30 games I had to re-add manually? It certainly was worth it timewise.  

Gameye's database kinda sucks in comparison all things considered <sub>(There's no PAL region, only UK for some reason?)</sub>, but for a free offering I consider it more than good enough.  

#

<sup id="note-1">[\*](#ref-1) The export is through the web/cloud instead of the app so it could theoretically be turned off at any point, but I gotta give props to the devs for having the option available! </sup>  
<sup id="note-2">[\*\*](#ref-2) I have to mention the app has a free 7-day trial, so I effectively paid **nothing** to scan my entire collection, export the data and fuck off somewhere else. The CLZ app really doesn't feel predatory and the subscription is probably there to fund server infrastructure, commercial barcode databases or something... I still don't want to pay it tho 😤 </sup>  
<sup id="note-3">[\*\*\*](#ref-3) Gameye however also has a **cartridge scanner**, which I used after all this database fudging to catalog my handheld games. It's...not very good either, but I got maybe a fourth of my Game Boy collection in through it? Better than nothing. </sup>    