__author__ = 'Basti'
import logging
import requests
from lxml import etree, html

rss_mappings = {
 u'feed/http://www.thenakedscientists.com/naked_scientists_podcast.xml': '//p[@class="bodytext"]',
 u'feed/http://feeds.feedburner.com/ClPlBl': None,
 u'feed/http://www.heise.de/newsticker/heise-atom.xml': '//p/..',
 u'feed/http://dzone.com/mz/agile/rss': '//p/..',
 u'feed/http://de.engadget.com/rss.xml': '//div[@class="copy post-body"]',
 u'feed/http://feeds.guardian.co.uk/theguardian/world/rss': '//p/..',
 u'feed/https://portal.mytum.de/rssPresse': '//div[@id="news-content"]',
 u'feed/http://www.guardian.co.uk/science/rss': '//p/..',
 u'feed/http://thehouseofportable.blogspot.com/feeds/posts/default': None,
 u'feed/http://feeds.theinquirer.net/feed/vnunet/the_INQUIRER': '//p/..',
 u'feed/http://www.hardwareboard.eu/external.php?do=rss&type=newcontent&sectionid=22&days=120&count=10': '//div[@class="entry-content"]//p',
 u'feed/http://feeds.feedburner.com/RichardWisemansBlog?format=xml': '//div[@class="entry-content"]//p',
 u'feed/https://portal.mytum.de/studium/preise/asRss': None,
 u'feed/https://portal.mytum.de/newsboards/news_students/asRss': '//div[@id="news-content"]//p',
 u'feed/https://wiki.stusta.mhn.de/Spezial:Semantische_Suche/-5B-5BKategorie:News-5D-5D/-3FTitel/-3FDatum/-3FAutor/-3FZusammenfassung/-3FBild/order%3DDESC/sort%3DDatum/format%3Drss': None,
 u'feed/https://www.computerbase.de/rss/news.xml': '//div[@class="text-content"]//p',
 u'feed/http://www.tagesschau.de/xml/rss2': '//div[@class="beitrag"]//p',
 u'feed/https://www.in.tum.de/index.php?id=106&type=100': '//div[@class="news-shorttext"]//p',
 u'feed/http://www.tv48erlangen-badminton.de/cms/?feed=rss2': '//div[@class="entry"]//p',
 u'feed/http://www.heise.de/tp/news-atom.xml': '//div[@class="pos-content artext"]//p',
 u'feed/http://mpi.fs.tum.de/fsmpi/RSS': None,
 u'feed/http://portableapps.com/blog/2/feed': None,
 u'feed/http://www.anandtech.com/rss/': None,
 u'feed/http://portableappz.blogspot.com/feeds/posts/default': None,
 u'feed/http://feeds2.feedburner.com/mydealz': '//div[@class="section-sub text--word-wrap"]',
 u'feed/http://www.hardware-infos.com/rss/news.xml': '//div[@class="post"]',
 u'feed/http://newsfeed.zeit.de/index': '//div[@class="article-body"]//p',
 u'feed/http://www.engadget.com/rss.xml': '//div[@class="copy post-body"]//p',
 u'feed/http://www.hardwareluxx.de/index.php/rss/feed/3.html': '//div[@itemprop="articleBody"]',
 u'feed/https://www.computerbase.de/rss/artikel.xml': None,
 u'feed/http://feeds.gawker.com/lifehacker/full': '//div[@class="post-content entry-content  new-annotation"]//p',
 u'feed/http://rss.golem.de/rss.php?feed=RSS2.0': '//div[@class="formatted"]//p',
 u'feed/http://googleblog.blogspot.com/feeds/posts/default': None,
 u'feed/http://rivva.de/rss.xml': '//article//a/@href',
 u'feed/https://xkcd.com/rss.xml': '//div[@class=""]//p',
 u'feed/http://static.winfuture.de/feeds/WinFuture-News-atom1.0.xml': '//div[@id="news_content"]/text()',
 u'feed/https://news.ycombinator.com/rss': None,
 u'feed/http://www.urlaubspiraten.de/feed': '//div[@class="sPost-ct editor"]//p',
 u'feed/http://www.prad.de/feed_10.xml': '//span[@class="news-content"]/div/text()',
 u'feed/https://www.siemens.com/press/apps/PageRss/de/pressrelease.php?content[]=CC&content[]=E&content[]=ES&content[]=EH&content[]=EP&content[]=ET&content[]=EW&content[]=H&content[]=HAU&content[]=HCP&content[]=HCX&content[]=HDX&content[]=HIM&content[]=I&content[]=ICS&content[]=IDT&content[]=IIA&content[]=IMT&content[]=IC&content[]=ICBT&content[]=ICLMV&content[]=ICMOL&content[]=ICRL&content[]=ICSG': None,
 u'feed/http://www.manager-magazin.de/news/index.rss': '//div[@class="mmArticleColumnInner"]//p',
 u'feed/http://suche.sueddeutsche.de/rss/Topthemen': '//section[@class="body"]/p',
 u'feed/http://www.tomshardware.de/feeds/atom/all.xml': '//article[@id="news-content"]//p',
 u'feed/http://www.in.tum.de/index.php?id=198&type=100': '//div[@id="maincontent"]//p',
 u'feed/http://vr-zone.com/feed': '//div[@class="post-content entry-content"]/p',
 u'feed/http://bjgoesnz.wordpress.com/feed/': '//div[@class="entry-content"]//p',
 u'feed/http://www.test.de/rss/alles/': '//div[@id="primary"]//p',
 u'feed/http://www.techhive.com/index.rss': '//section[@class="page"]',
 u'feed/http://www.bwfbadminton.org/feed/news.aspx?id=4': '//div[@class="body"]',
 u'feed/http://blog.foundationdb.com/rss.xml': '//div[@class="section post-body"]',
}


def get_rss_content(stream_id, url):
    result = ""
    if rss_mappings.get(stream_id, None):
        try:
            print url  # For Debugging purposes
            html_src = requests.get(url).content
            xpath = rss_mappings[stream_id]
            parsed_tree = html.document_fromstring(html_src)
            nodes = parsed_tree.xpath(xpath)

            result = " <br> " .join([etree.tostring(node) for node in nodes])

        except Exception as e:
            try:
                result = " ".join(nodes)
            except Exception as e:
                logging.error(e.message)

    return result