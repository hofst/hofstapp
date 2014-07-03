__author__ = 'Basti'

from feedly import FeedlyClient
import stopwords
from Scraper import Scraper
from rss_mappings import get_rss_content
from feedly_credentials import *

memcache = memcache.Client(pickleProtocol=1)

if FEEDLY_ACCESS_TOKEN:
    feedly_client = FeedlyClient(access_token=FEEDLY_ACCESS_TOKEN, sandbox=False)
else:
    feedly_client = FeedlyClient(
        client_id=FEEDLY_CLIENT_ID,
        client_secret=FEEDLY_CLIENT_SECRET,
        sandbox=True
    )

class Subscriptions(ndb.Model):
    pass

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
    crawled = ndb.DateTimeProperty()
    unread = ndb.BooleanProperty()
    keywords = ndb.StringProperty(repeated=True)
    image = ndb.StringProperty()

    @staticmethod
    def QUERY():
        return News.query(News.crawled > datetime.now() - timedelta(days=2)).order(-News.crawled)

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
            crawled = datetime(1970, 1, 1) + timedelta(milliseconds=dic.crawled),
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

def callback():
    code = request.vars.get('code')

    if not code:
        redirect("/welcome/feedly/")

    res = feedly_client.get_access_token(FEEDLY_REDIRECT_URI, code)
    if res.get('errorCode') == 400:
        redirect("/welcome/feedly/")

    redirect("/welcome/feedly/?access_token=%s" % feedly_client.access_token)

def index():
    if not feedly_client.access_token:
        if not request.vars.access_token:
            # Redirect the user to the feedly authorization URL to get user code
            code_url = feedly_client.get_code_url(FEEDLY_REDIRECT_URI)
            return redirect(code_url)
        else:
            feedly_client.access_token = request.vars.access_token

    return dict(news=News.get())

def update_news():
    news = [News.from_dict(news_dic) for news_dic in feedly_client.get_news_dics()]
    existing_news = set(News.query(News.datetime > datetime.now() - timedelta(days=2)).fetch(keys_only=True))
    print "Existing news: %s" % len(existing_news)
    news = [n for n in news if n.key not in existing_news]
    print "Putting %s news" % len(news)
    ndb.put_multi(news)
    for n in news:
        taskqueue.add(url="/welcome/feedly/get_content", params={"news_key": n.key.urlsafe()})
    feedly_client.mark_article_read([n.key.id() for n in news])

def get_content():
    news = ndb.Key(urlsafe=request.vars.news_key).get()
    content = get_rss_content(news.origin_stream_id, news.link)
    if content:
        news.content = content
        news.put()

def schedule_update_news():
    try:
        taskqueue.add(url="/welcome/feedly/update_news")
    except Exception as e:
        logging.error("taskqueue add error: " + e.message)