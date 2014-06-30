__author__ = 'Basti'

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
    print "Putting %s news" % len(news)
    ndb.put_multi(news)
    for n in news:
        taskqueue.add(url="/welcome/feedly/get_content", params={"news_key": n.key.urlsafe()})
    feedly_client.mark_article_read([n.key.id() for n in news])

def get_content():
    news = ndb.Key(urlsafe=request.vars.news_key).get()
    news.content = get_rss_content(news.origin_stream_id, news.link) or news.content
    news.put()