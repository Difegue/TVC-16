Title: Updating the TVC-16 to Caddy 2
Date: 2021-07-06 22:00
Category: Software
Tags: docker, goatcounter, caddy, webhook
Slug: caddy-2-update
Authors: Difegue
HeroImage: images/tamamo.jpg  
Summary: Put on some music and spend a comfy evening whooping out some webhook wizardry. 🧙‍♂️

[Caddy 2](https://caddyserver.com/v2) has been out for a little more than a year and I finally got off my ass to update my server setup. 🤠  
Feel free to read the [OG post](./blogopolis-docker) about the Caddy 1 setup to get some extra context.  

# Updating the Caddyfile  

For non-initiates, the [Caddyfile](https://caddyserver.com/docs/caddyfile) is essentially the entire server configuration.
There's surprisingly little changes to it!  
I essentially went from something like this:  

~~~~javascript
tvc-16.science, www.tvc-16.science {
    tls *******
    root /var/www/html
    git {
        repo     github.com/difegue/TVC-16
        branch   gh-pages
        pull-args --allow-unrelated-histories -s recursive -X theirs
        hook /webhook mywebhooksecret
    }
}

lrr.tvc-16.science {
    tls *******
    proxy / localhost:3000
}

diy.tvc-16.science {
    tls *******
    proxy / localhost:8080
}

dingus.tvc-16.science {
    tls *******
    proxy / localhost:7777 {
        header_upstream Host {host}
        header_upstream X-Real-IP {remote}
        header_upstream X-Forwarded-For {remote}
        header_upstream X-Forwarded-Proto {scheme}
  }
}
~~~~  

To this:  

~~~~javascript
tvc-16.science {
    tls *******
    root * /var/www/html
    file_server
}

www.tvc-16.science {
    redir https://tvc-16.science{uri}
}

lrr.tvc-16.science {
    tls *******
    reverse_proxy localhost:3000
}

diy.tvc-16.science {
    tls *******
    reverse_proxy localhost:8080
}

dingus.tvc-16.science {
    tls *******
    reverse_proxy localhost:7777 {
        header_up X-Real-IP {http.request.remote}
        header_up X-Forwarded-For {http.request.remote}
  }
}
~~~~

The reverse proxies map as-is, and the configuration to make my [GoatCounter](https://github.com/zgoat/goatcounter) instance work correctly is actually even simpler, since Caddy v2 passes [most headers through now.](https://github.com/caddyserver/caddy/issues/2873)  

But as you might've noticed, the `git` section which automatically updated the static pages you're reading right now...is gone! 👻

# Swapping out my Webhook Implementation  

As a quick refresher for how the `git` integration worked (read the Caddy 1 post for more details!):  

* When the TVC-16 [Git repo](https://github.com/Difegue/TVC-16) is updated, GitHub sends a `POST` request to a `tvc-16.science` subdomain, triggering a pull of the updated repo's `gh-pages` branch, which contains the static HTML files for the blog, built with [Pelican](https://blog.getpelican.com/).  

With Caddy 1, it was super easy to use the built-in [git plugin](https://web.archive.org/web/20190131203258/https://caddyserver.com/docs/http.git) to setup a built-in webhook endpoint that Github could then hit. Sadly, Caddy 2 doesn't bundle a git plugin anymore! 😢  

You can use a [community one](https://caddy.community/t/v2-git-webhooks/10207) if you build your Caddy yourself (`xcaddy` is a very nice tool to do that), but I don't really fancy rebuilding my webserver myself whenever I want to update.  

So, I switched to a **standalone server** to handle webhooks!  
To keep with the theme of _"I guess I'm using stuff written in Go now"_, I went with [webhook.](https://github.com/adnanh/webhook) <sub>very original name and not confusing at all thanks</sub>  
`webhook` is sadly a bit more verbose to setup than the ole Caddy integration, but the overall concept is the same:  

1️⃣ Setup your hook's ID and rules in a `hooks.json` file, to run a git pull in `/var/www/html` when it's hit:  
~~~~javascript
[
    {
        "id": "mikon",
        "execute-command": "/usr/local/bin/update_static.sh",
        "command-working-directory": "/var/www/html",
        "trigger-rule": {
            "and": [
                {
                    "match": {
                        "type": "payload-hash-sha1",
                        "secret": "TheWebHookSecret",
                        "parameter": {
                            "source": "header",
                            "name": "X-Hub-Signature"
                        }
                    }
                },
                {
                    "match": {
                        "type": "value",
                        "value": "refs/heads/gh-pages",
                        "parameter": {
                            "source": "payload",
                            "name": "ref"
                        }
                    }
                }
            ]
        }
    }
]
~~~~

It's easier to use a bash script as the `execute-command` here since `webhook` doesn't accept inline arguments, but the script itself is just a one-liner:  
```
#!/bin/bash

# This runs in /var/www/html, which already contains an initialized copy of the git repo.
git pull --allow-unrelated-histories -s recursive -X theirs
```

2️⃣ Start the `webhook` server:  

```
webhook -hooks hooks.json -port 4000 -verbose
```

3️⃣ Add a subdomain to your website and your Caddyfile to reverse-proxy it:  

```
tamamo.tvc-16.science {
    tls *******
    reverse_proxy localhost:4000
}
```  

4️⃣ Add the webhook to your GitHub repo, and you're done!  

Since it goes through Caddy, you get SSL verification that _just works_ out of the box.  
![🦊 mikon!]({static}/images/webhook.png)  
GitHub actually sends *two* POST requests (one when `master` is pushed, and one when `gh-pages` is updated by GitHub Actions), but `webhook` will filter the first one out since it doesn't match the `refs/heads/gh-pages` rule.  

```
[webhook] 2021/07/05 23:36:50 [8a4b2a] finished handling mikon
[webhook] 2021/07/05 23:39:01 Started POST /hooks/mikon
[webhook] 2021/07/05 23:39:01 [b556e5] incoming HTTP request 
[webhook] 2021/07/05 23:39:01 [b556e5] mikon got matched
[webhook] 2021/07/05 23:39:01 [b556e5] mikon got matched, but didn't get triggered because the trigger rules were not satisfied
[webhook] 2021/07/05 23:39:01 Completed 200 OK in 11.868297ms
```

# Closing thoughts

I was kinda worried about redoing the autodeploy setup as Caddy 2 doesn't support it out of the box, but `webhook` seems to be a solid alternative.  
Not having to replace it again whenever I end up re-switching HTTP servers is also a bonus!  

The usual way of deploying this static blog stuff is to do the Pelican build on the host machine directly instead of using CI, but I prefer putting the grunt work outside of this woefully underpowered 3$ VPS that's already running about 5 services too many.  

Here's a Tamamo for having made it to the end.  
![UNIXCHADS win yet again!]({static}/images/tamamo.jpg)  
