#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'dfug'
SITENAME = u'Blogopolis'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None 
AUTHOR_FEED_RSS = None

# Blogroll
MENUITEMS = (('Projects', '/projects.html'),
         ('Articles', '/'),
         ('Categories', '/categories.html'),)

# custom page generated with a jinja2 template
TEMPLATE_PAGES = {'projects.html': 'projects.html'}

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
DISPLAY_CATEGORIES_ON_MENU = False
THEME = "./theme"
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
