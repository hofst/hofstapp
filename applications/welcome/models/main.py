# -*- coding: UTF-8 -*-
__author__ = 'Basti'

from feedly import FeedlyClient
import stopwords
from gluon.storage import Storage
from datetime import datetime, timedelta
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
import logging
from pprint import pprint
from collections import OrderedDict
memcache = memcache.Client(pickleProtocol=1)

FEEDLY_REDIRECT_URI = "http://localhost"
FEEDLY_CLIENT_ID="sandbox"
FEEDLY_CLIENT_SECRET="ES3R6KCEG46BW9MYD332"
FEEDLY_ACCESS_TOKEN="AjaGzax7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQxMTgxMTU2MDIxOSwiaSI6IjUwZjJiYzYxLTkwY2QtNDcwNC1iNmJhLWY2N2UyZTg2MThiNCIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwieCI6InN0YW5kYXJkIn0:feedlydev"  # sebastian@hofst.com
# FEEDLY_ACCESS_TOKEN = "AjPNcgp7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQxMTc2NTg1ODE2OSwiaSI6ImY2ZmI4ZWEzLTBjNDItNDMwYy04M2RkLWM0MzViNThjYzMyZCIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwieCI6InN0YW5kYXJkIn0:feedlydev"  # basti@katseb.de
# FEEDLY_ACCESS_TOKEN = ""

if FEEDLY_ACCESS_TOKEN:
    feedly_client = FeedlyClient(access_token=FEEDLY_ACCESS_TOKEN, sandbox=False)
else:
    feedly_client = FeedlyClient(
        client_id=FEEDLY_CLIENT_ID,
        client_secret=FEEDLY_CLIENT_SECRET,
        sandbox=True
    )

class News(ndb.Model):
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    origin_id = ndb.StringProperty()
    origin_stream_id = ndb.StringProperty()
    origin_title = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    link = ndb.StringProperty()
    author = ndb.StringProperty()
    pubDate = ndb.DateTimeProperty()
    unread = ndb.BooleanProperty()
    keywords = ndb.StringProperty(repeated=True)
    image = ndb.StringProperty()

    @staticmethod
    def QUERY():
        return News.query(News.datetime > datetime.now() - timedelta(days=2)).order(-News.datetime)

    @staticmethod
    def from_dict(dic):
        return News(
            key=ndb.Key(News, dic.id),
            origin_id = dic.originId,
            origin_stream_id = dic.origin["streamId"],
            origin_title = dic.origin["title"],
            title = dic.title,
            content = dic.summary.get("content") if dic.summary else "",
            link = dic.alternate[0]["href"] if dic.alternate else "",
            author = dic.author,
            pubDate = datetime(1970, 1, 1) + timedelta(milliseconds=dic.published),
            unread = dic.unread,
            keywords = dic.keywords if dic.keywords else [],
            image = dic.enclosure[0]["href"] if dic.enclosure else dic.visual["url"] if dic.visual else ""
        )

    @staticmethod
    def get():
        return News.QUERY().fetch()
        news = OrderedDict()

        for n in News.QUERY().fetch():
            token = repr(stopwords.normalize(n.title + " " + n.content))
            news.setdefault(token, [])
            news[token] += [n]

        return [n[0] for n in news.values()]