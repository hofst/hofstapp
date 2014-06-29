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

    feeds = [Storage(feed) for feed in feedly_client.get_user_subscriptions()][:2]
    for feed in feeds:
        feed.pubDate = datetime(1, 1, 1) + timedelta(microseconds=feed.updated)
        feed_items = [Storage(item) for item in feedly_client.get_feed_content(feed.id)["items"]]
        feed.feed_items = []
        for item in feed_items:
            new_item = Storage()
            new_item.title = item.title
            new_item.content = item.summary.get("content")
            new_item.link = item.alternate[0]["href"] if item.alternate else ""
            new_item.author = item.author
            new_item.guid = item.id
            new_item.pubDate = datetime(1, 1, 1) + timedelta(microseconds=item.published)
            new_item.unread = item.unread
            new_item.keywords = item.keywords
            new_item.image = item.enclosure[0]["href"] if item.enclosure else item.visual["url"] if item.visual else ""
            feed.feed_items += [new_item]
    return dict(feeds=feeds)