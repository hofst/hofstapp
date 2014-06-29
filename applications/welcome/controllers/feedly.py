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