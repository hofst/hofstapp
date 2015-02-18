# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Sebastian Hofstetter'

import logging
import requests
from lxml import etree, html

rss_mappings = {
    u'feed/http://www.thenakedscientists.com/naked_scientists_podcast.xml': dict(content='//ul[contains(@class, "result")]', image='//img[contains(@class, "teaser")]/@src', redirect='//h4/a[contains(@href, "transcript")]/@href'),
    u'feed/http://feeds.feedburner.com/ClPlBl': dict(image='//img[@class="header-logo1"]/@src'),
    u'feed/http://www.heise.de/newsticker/heise-atom.xml': dict(content='//div[@class="meldung_wrapper"]', image='//figure[@class="aufmacherbild"]/img/@src'),
    u'feed/http://dzone.com/mz/agile/rss': dict(content='(//div[@class="content"])[1]', image='id("logo-dzone-new")/a/img/@src'),
    u'feed/http://de.engadget.com/rss.xml': dict(content='//div[@itemprop="articleBody"]'),
    u'feed/http://feeds.guardian.co.uk/theguardian/world/rss': dict(content='//article', image='(//article//img)[1]/@src'),
    u'feed/http://www.guardian.co.uk/science/rss': dict(content='//article', image='(//article//img)[1]/@src'),
    u'feed/http://thehouseofportable.blogspot.com/feeds/posts/default': dict(),
    u'feed/http://feeds.theinquirer.net/feed/vnunet/the_INQUIRER': dict(content='//div[@class="contenttop_text"]'),
    u'feed/http://www.hardwareboard.eu/external.php?do=rss&type=newcontent&sectionid=22&days=120&count=10': dict(content='//div[@class="entry-content"]', image='//img[contains(@class, "wp-post-image")]/@src'),
    u'feed/http://feeds.feedburner.com/RichardWisemansBlog?format=xml': dict(content='//div[@class="entry-content"]'),
    u'feed/https://www.computerbase.de/rss/news.xml': dict(content='//div[@class="text-content"]', image='//img[@class="logo"]/@src'),
    u'feed/http://www.tagesschau.de/xml/rss2': dict(content='//div[@class="box"]/p', image='(//img[@class="img"])[1]/@src'),
    u'feed/http://www.tv48erlangen-badminton.de/cms/?feed=rss2': dict(content='//div[@class="entry"]'),
    u'feed/http://www.heise.de/tp/news-atom.xml': dict(content='//div[@class="pos-content artext"]', image='//img[@class="tp-img"]/@src'),
    u'feed/http://mpi.fs.tum.de/fsmpi/RSS': dict(content='id("content")'),
    u'feed/http://portableapps.com/blog/2/feed': dict(content='//div[@class="content"]/p', image='id("mainlogo")/@src'),
    u'feed/http://www.anandtech.com/rss/': dict(),
    u'feed/http://portableappz.blogspot.com/feeds/posts/default': dict(),
    u'feed/http://feeds2.feedburner.com/mydealz': dict(content='//div[@class="section-sub"]'),
    u'feed/http://www.hardware-infos.com/rss/news.xml': dict(content='//div[@class="post"]'),
    u'feed/http://newsfeed.zeit.de/index': dict(content='//div[@class="article-body"]'),
    u'feed/http://www.engadget.com/rss.xml': dict(content='//div[@class="article-content"]'),
    u'feed/http://www.hardwareluxx.de/index.php/rss/feed/3.html': dict(content='//div[@itemprop="articleBody"]', image='(//div[@itemprop="articleBody"]//img/@src)[1]'),
    u'feed/https://www.computerbase.de/rss/artikel.xml': dict(content='id("article_passages")', image='(id("article_passages")//img)[1]/@src'),
    u'feed/http://feeds.gawker.com/lifehacker/full': dict(content='//div[contains(@class, "post-content")]', image='(//div[contains(@class, "post-content")]//img)[1]/@src'),
    u'feed/http://rss.golem.de/rss.php?feed=RSS2.0': dict(content='//div[@class="formatted"]', image='(//img)[2]/@src'),
    u'feed/http://googleblog.blogspot.com/feeds/posts/default': dict(),
    u'feed/http://rivva.de/rss.xml': dict(redirect='//article//a/@href'),
    u'feed/https://xkcd.com/rss.xml': dict(),
    u'feed/http://static.winfuture.de/feeds/WinFuture-News-atom1.0.xml': dict(content='id("news_content")', image='(id("news_content")//img)[1]/@src'),
    u'feed/https://news.ycombinator.com/rss': dict(),
    u'feed/http://www.urlaubspiraten.de/feed': dict(content='//div[@class="sPost-ct editor"]', image='(//div[@class="sPost-ct editor"]//img)[1]/@src'),
    u'feed/http://www.prad.de/feed_10.xml': dict(content='(//span[@class="news-content"])[2]'),
    u'feed/https://www.siemens.com/press/apps/PageRss/de/pressrelease.php?content[]=CC&content[]=E&content[]=ES&content[]=EH&content[]=EP&content[]=ET&content[]=EW&content[]=H&content[]=HAU&content[]=HCP&content[]=HCX&content[]=HDX&content[]=HIM&content[]=I&content[]=ICS&content[]=IDT&content[]=IIA&content[]=IMT&content[]=IC&content[]=ICBT&content[]=ICLMV&content[]=ICMOL&content[]=ICRL&content[]=ICSG': dict(),
    u'feed/http://www.manager-magazin.de/news/index.rss': dict(content='//div[@class="mmArticleColumnInner"]'),
    u'feed/http://suche.sueddeutsche.de/rss/Topthemen': dict(content='//section[@class="body"]'),
    u'feed/http://www.tomshardware.de/feeds/atom/all.xml': dict(content='//article[@id="news-content"]'),
    u'feed/http://www.in.tum.de/index.php?id=198&type=100': dict(content='//div[@id="maincontent"]'),
    u'feed/http://vr-zone.com/feed': dict(content='//div[@class="post-content entry-content"]'),
    u'feed/http://bjgoesnz.wordpress.com/feed/': dict(content='//div[@class="entry-content"]'),
    u'feed/http://www.test.de/rss/alles/': dict(),
    u'feed/http://www.techhive.com/index.rss': dict(content='//section[@class="page"]'),
    u'feed/http://www.bwfbadminton.org/feed/news.aspx?id=4': dict(content='//div[@class="body"]'),
    u'feed/http://blog.foundationdb.com/rss.xml': dict(content='//div[@class="section post-body"]'),
    u'feed/http://www.tum.de/die-tum/aktuelles/?no_cache=1&type=100': dict(content='//div[@class="news-single-item"]')
}


def make_url_absolute(top_url, relative_url):
    """
    >>> make_url_absolute("//web.de/jkl/a", "/test/asd?sdf#q")
    'http://web.de/test/asd?sdf#q'
    >>> make_url_absolute("//web.de/jkl/a", "https://test.de/test/asd?sdf#q")
    'https://test.de/test/asd?sdf#q'
    >>> make_url_absolute("//web.de/jkl/a", "//test.de/test/asd?sdf#q")
    'http://test.de/test/asd?sdf#q'
    >>> make_url_absolute("https://web.de/jkl/a", "//test.de/test/asd?sdf#q")
    'https://test.de/test/asd?sdf#q'
    """

    from urlparse import urlparse
    parsed_top_url = urlparse(top_url)
    parsed_relative_url = urlparse(relative_url)

    if parsed_relative_url.netloc:
        # url is already absolute
        scheme = parsed_relative_url.scheme or parsed_top_url.scheme or "http"  # default scheme to http
        return scheme + '://{relative.netloc}{relative.path}?{relative.query}#{relative.fragment}'.format(top=parsed_top_url, relative=parsed_relative_url)
    else:
        scheme = parsed_top_url.scheme or "http"  # default scheme to http
        return scheme + '://{top.netloc}{relative.path}?{relative.query}#{relative.fragment}'.format(top=parsed_top_url, relative=parsed_relative_url)


def rescrap_news(n):
    mapping = rss_mappings.get(n.origin_stream_id, None)
    if mapping:
        try:
            logging.info(n.link)
            html_src = requests.get(n.link).content
            parsed_tree = html.document_fromstring(html_src)
            if "redirect" in mapping:
                red = parsed_tree.xpath(mapping["redirect"])[0]
                n.link = make_url_absolute(n.link, red)
                logging.info(n.link)
                html_src = requests.get(n.link).content
                parsed_tree = html.document_fromstring(html_src)

            if "content" in mapping:
                nodes = parsed_tree.xpath(mapping["content"])
                n.content = " <br> ".join([etree.tostring(node) for node in nodes])

            if "image" in mapping:
                n.image = parsed_tree.xpath(mapping["image"])[0]
                n.image = make_url_absolute(n.link, n.image)

        except Exception as e:
            logging.error(e.message)
        n.put()
