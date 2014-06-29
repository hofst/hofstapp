__author__ = 'Basti'

from feedly import FeedlyClient
from gluon.storage import Storage
from datetime import datetime, timedelta
from google.appengine.api import memcache
import logging
memcache = memcache.Client(pickleProtocol=1)


FEEDLY_REDIRECT_URI = "http://localhost"
FEEDLY_CLIENT_ID="sandbox"
FEEDLY_CLIENT_SECRET="ES3R6KCEG46BW9MYD332"
FEEDLY_ACCESS_TOKEN="AjaGzax7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQxMTgxMTU2MDIxOSwiaSI6IjUwZjJiYzYxLTkwY2QtNDcwNC1iNmJhLWY2N2UyZTg2MThiNCIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwieCI6InN0YW5kYXJkIn0:feedlydev"
FEEDLY_ACCESS_TOKEN = ""

if FEEDLY_ACCESS_TOKEN:
    feedly_client = FeedlyClient(access_token=FEEDLY_ACCESS_TOKEN, sandbox=False)
else:
    feedly_client = FeedlyClient(
        client_id=FEEDLY_CLIENT_ID,
        client_secret=FEEDLY_CLIENT_SECRET,
        sandbox=True
    )