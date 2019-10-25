Title: Deploying an ephemeral macOS environment through Github Actions
Date: 2019-10-25 00:00  
Category: Cool Tricks  
Tags: github actions, apple, macos, vm, homebrew
Slug: mac-github-actions
Authors: Difegue  
HeroImage: images/macactions.png  
Summary: I don't think they meant this when they said "Think Different".  

Oh no! Someone's giving me [macOS stuff to test](https://github.com/Difegue/LANraragi/pull/221) and I don't have access to any Mac whatsoever this weekend!  
_What in the doushio can I do?_  

Most solutions for getting a virtualized Mac running involve downloading the 7GB-something setup from Apple, installing it in [some form of virtualization](https://github.com/foxlet/macOS-Simple-KVM) software, setting up a bunch of bullshit magical variables to masquerade your VM as an iMac and then waiting through the entire installation process.  

Past that, you'll also need to add an Apple Account, download Xcode and its glorious 6 GBs of awful IDE design, etc etc _jesus this is going to eat my entire weekend_  
<sub><sup>you can technically only download the xcode command line tools and they're like 200MBs but I'm trying to overdramatize a bit here</sup></sub>  

The other solution is of course to rent a Mac VPS, but as this is a super niche market, prices are [atrociously expensive](https://www.macstadium.com/pricing) for what amounts to me running `homebrew` for about 30 minutes.  

## Jumping into Actions

Since GitHub Actions introduced matrix builds recently, there very conveniently are [macOS runners](https://help.github.com/en/github/automating-your-workflow-with-github-actions/software-in-virtual-environments-for-github-actions#macos-1014) for me to run code on. And they come with a **lot** of devtools preinstalled, making for a rather comfy experience.  

At this point I could just write an Actions script running my `homebrew` code and be done with it, but I thought I could have something a bit more flexible.  
Hot off the trail of [my last Actions venture](./lcl-pebble.html), I thought about using the [tmate](https://github.com/marketplace/actions/debugging-with-tmate) action to spawn a SSH session on the Mac runner for me. It'd basically give me an **on-demand, pre-provisioned** macOS command line whenever I'd want!  

![ANYTHING]({static}/images/anything.jpg)  
<sub><sup>For up to 6 hours of execution time but honestly that's already way too much </sup></sub>  

## Writing the Action

Using the tmate action as-is would basically make this setup dead simple, but it [doesn't work on Mac runners as-is.](https://github.com/mxschmitt/action-tmate/issues/3) Darn.  

Luckily the entire action is really easy to replicate in bash, so I just wrote my own:  

```yaml
name: Summon Steve Jobs

on: [push]

jobs:
  build:

    runs-on: macOS-10.14

    steps:
    - uses: actions/checkout@v1
    - name: Install tmate
      run: |
        brew install tmate openssh screenfetch
        echo -e 'y\n'|ssh-keygen -q -t rsa -N "" -f ~/.ssh/id_rsa
        tmate -S /tmp/tmate.sock new-session -d
        tmate -S /tmp/tmate.sock wait tmate-ready
    - name: It just works
      run: |
        screenfetch
        SSH="$(tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}')"
        WEB="$(tmate -S /tmp/tmate.sock display -p '#{tmate_web}')"
        echo "SSH: ${SSH}"
        echo "Web: ${WEB}"
        echo "You can now connect to the tmate session."
        while true; do 
          # loop infinitely
          sleep 10
        done
```

The only issue here is that quitting the session doesn't automatically end the run like the original action does, but it's good enough.™  

![rebel rebel how could they know]({static}/images/macactions.png)

## Spare Thoughts

I was curious about whether you could get VNC output on this, but while the command to enable VNC works, the runners don't expose anything for you to connect to.

Since I wanked this to debug the upcoming Homebrew support for LRR, it's totally legal and not breaking the [Actions TOS](https://help.github.com/en/github/automating-your-workflow-with-github-actions/about-github-actions#usage-limits) in any way. 😇  
