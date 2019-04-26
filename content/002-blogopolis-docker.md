Title: Building this blog with Pelican, Github Actions and Caddy
Date: 2019-04-25 22:00
Category: Docker
Tags: docker, pelican, caddy, github actions
Slug: blogopolis-docker
Authors: Difegue
Summary: Writing this also allows me to check that this continuous integration thingamabob is working as expected.

The original, blogless iteration of TVC-16 was hosted on a bog-standard Apache2 server. [My](https://lrr.tvc-16.science) [subdomains](https://diy.tvc-16.science) are all directly linked to Docker containers, so that very basic configuration was enough.  

For blog articles though, I really wanted to have something easier on the server maintenance than having to scp my html by hand. I originally considered using [Ghost](https://ghost.org/) in yet another Docker container and doing all my writing in it, but it'd eventually be a pain to export/reimport all the data in case of a server switch.  

I decided to use a static site generator like all the nerds instead and went with [Pelican](https://blog.getpelican.com/). Classic stuff so far, but I don't think many people are using [Github Actions](https://github.com/features/actions/) for their deployments yet despite the fact it's **r a d**! <sub><sup>well the fact it's in beta might be a blocker too for some people</sup></sub>

# Building in Pelican
I didn't do anything out of the ordinary in the Pelican side -- this is a hella standard blog if you ignore the theme. (Which I wholelifted from the previous nonblog version, so I can thank 2018 myself for putting in all the CSS work).  

The only thing I did that's kinda obscure unless you read the Pelican configuration file specs is having a custom template render to a custom page (the Projects):

~~~~
# custom page generated with a jinja2 template
TEMPLATE_PAGES = {'projects.html': 'projects.html'}
~~~~

I dropped the entire Pelican sources into a [Github repo](https://github.com/Difegue/TVC-16), and now it's on to the fun part:

# Hot Github integrations

I already have some experience in GH Actions from writing the test suite for [LANraragi](https://github.com/Difegue/LANraragi), so I was expecting the setup time for this to be fairly quick. Turns out it went faster than expected!  

![hot github actions near your town]({static}/images/tvc-16-actions.png)  

This building process is triggered on every push to _master_ and is as simple as it looks:

* Step 1: Run Pelican on the repo to build the website. This is [super basic](https://github.com/Difegue/TVC-16/tree/master/.github/action-pelican), I'm just grabbing a pelican docker image and building away.
* Step 2: Force-push the built _output_ folder to the _gh-pages_ branch of the repo.

The output branch is named _gh-pages_ because I conveniently re-used an [https://github.com/JasonEtco/push-to-gh-pages](existing Action) to go faster. I don't actually use Github Pages but hey, no harm done!

Another integration I made is through the comment system -- The way Microsoft made its MSDN comment system [basically just Github Issues](https://docs.microsoft.com/en-us/teamblog/a-new-feedback-system-is-coming-to-docs) is pretty inspiring.[https://utteranc.es/](Utterances) is an open source variant which I added to my Pelican template in about 5 seconds.  

As a result, all the blog's data is backed up on Github. If I ever had to switch to another Git repo provider I'd likely lose the comments, but I'm banking on those not being too important.

# Deploying on TVC-16 through Caddy

A friend recently told me that I was being an old fart by still using Apache2 in _the current year_, so I swapped it out for [https://caddyserver.com/](Caddy). Caddy's big advantage here lies in its [`http.git`](https://caddyserver.com/docs/http.git)  plugin, which automagically pulls the latest built version of the website from Github.  

Here's the Caddyfile I use:

~~~~
tvc-16.science, www.tvc-16.science {
    root /var/www/html
    git {
        repo     github.com/difegue/TVC-16
	    branch   gh-pages
        pull-args --rebase --allow-unrelated-histories
    }
}
~~~~

The biggest issue I encountered here was that http.git does a `git clone` when deploying your website for the first time, then only does `git pull` to update it. Which is very sane if you're pulling the sources, then building the website on the server itself.  

What I'm pulling however is the already-built website, which is force-pushed by the Github Actions bot every time. As such, the Git history is getting continuously broken, making regular Git pulls fail instantly.

Adding the pull arguments you see above is enough to tell git "it's alright just stop caring". It's a bit weird using rebase here, but it masterfully dodges merge conflicts by using the new remote as a base and then replaying my "work" (aka nothing at all) on top of it.  

# Possible enhancements

http.git in its base configuration pulls from the remote repo every hour. You can add a webhook pretty easily to have it only trigger on pushes, but I haven't bothered yet.  


