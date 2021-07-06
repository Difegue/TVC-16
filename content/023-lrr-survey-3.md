Title: The 2021 LANraragi User Survey
Date: 2021-07-07 00:00  
Category: LANraragi  
Tags: lanraragi, survey, lookback
Slug: lrr-survey-3
Authors: Difegue  
HeroImage: images/lrr-survey/survey3-image.jpg  
Summary: The _absolute current state_ of the Perl5 manga reader device.  

![it's actually eternal summer but everyone chooses to forget about it]({static}/images/lrr-survey/summer.gif)  
It's summer! That means AC prices shooting up through the roof, major cities being deserted, and the yearly **LRR User Survey**.  
<sub>Pouring one out for my Canada homies currently dying under the heat dome</sub>  

The User Survey is a quick means for me to gauge how many users are out there (as the app itself has zero telemetry), and figure out which features are wanted to drive development forward.  

Here's a quick rundown of everything that landed between the [2020 Survey results](./lrr-survey-2-results.html) and the latest release, ["Lucy Can't Dance"](https://github.com/Difegue/LANraragi/releases/tag/v.0.7.9):  
![wow, cool reader!]({static}/images/lrr-survey/survey3-webapp.png)

* **Fully rewritten Web Reader**, with new options, tags shown in the page overlay, better keyboard shortcuts and built-in infinite scrolling!  
* **Clickable tags**, to trigger searches in a much easier fashion.
* **URL Downloading support**, with a matching [Browser Extension](https://github.com/Difegue/Tsukihi) to queue downloads directly from your Browser.
* **Column customization** on a namespace basis in the Index to expose your most important tags directly.
* More **external reader** work, with a new client for [iOS](https://github.com/Doraemoe/DuReader), and LRReader now available in the [Microsoft Store](https://www.microsoft.com/store/apps/9MZ6BWWVSWJH).  
* **Server-side progress tracking**, with an option to come back to client-side tracking for multi-user instances.
* Multiple improvements to Categories, by making them more accessible across the UI.
* Support for AVIF and HEIF, already covered by some external readers as well.
* Being able to **move the Thumbnail Directory** 🎊🎊🎊
* Offloading of many tasks to a Job Queue using [Minion](https://mojolicious.org/perldoc/Minion), to speed up many parts of the server.
* A Shinobu rewrite to avoid murdering hard drives on server restarts 🍩💿
* Basic support for FAKKU metadata.
* A [logo change](./lrr-icon-study.html)!

And even more stuff I can't write about, lest the blogpost triples in size!  

The downloader stuff took most of the work this year, although it has been infinitely useful to me at the very least, so I'm glad I put the time into it.  
I managed to tackle most of the asks from Survey 2 (with the help of a few contributors I am eternally thankful to have), with the exception of **duplicate detection**.  
That just means I get to put it again in the suggestions for this 2021 edition! :^)  

## [You can answer the survey here!](https://forms.office.com/r/8TVSTXKVsm)  

I've also added some new sticker designs to the [LRR Ko-Fi Shop](https://ko-fi.com/lanraragi/shop), if you'd like to sponsor development and get a little bonus out of it!  
The V2 logo sticker now has a clear background, so you can stickerbomb your old _lame stickers_ with the wonderful `vapor-retro-neumorphic` shapes of the LANraragi logo.  
![I really like my Perl 5 sticker and dread the day Perl 7 will finally release and make it obsolete]({static}/images/lrr-survey/survey3-image.jpg)