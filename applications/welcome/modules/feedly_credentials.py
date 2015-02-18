# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Sebastian Hofstetter'

import os

is_local = os.environ['SERVER_SOFTWARE'].find('Development') >= 0

FEEDLY_REDIRECT_URI = "http://localhost"
FEEDLY_CLIENT_ID="sandbox"
FEEDLY_CLIENT_SECRET="ES3R6KCEG46BW9MYD332"
FEEDLY_ACCESS_TOKEN="AmM71mh7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQzMTg4ODk3NDc5OCwiaSI6ImY2ZmI4ZWEzLTBjNDItNDMwYy04M2RkLWM0MzViNThjYzMyZCIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwidyI6IjIwMTMuMTQiLCJ4Ijoic3RhbmRhcmQifQ:feedlydev"  # basti@katseb.de

