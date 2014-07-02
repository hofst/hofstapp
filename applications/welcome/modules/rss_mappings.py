__author__ = 'Basti'
from Scraper import Scraper
from gluon.storage import Storage

rss_mappings = {
 u'feed/http://www.thenakedscientists.com/naked_scientists_podcast.xml': '//p[@class="bodytext"]//text()',
 u'feed/http://feeds.feedburner.com/ClPlBl': None,
 u'feed/http://www.heise.de/newsticker/heise-atom.xml': '//div[@class="meldung_wrapper"]//p//text()',
 u'feed/http://dzone.com/mz/agile/rss': '//div[@class="node node-page node-article"]//p//text()',
 u'feed/http://de.engadget.com/rss.xml': '//div[@class="copy post-body"]//text()',
 u'feed/http://feeds.guardian.co.uk/theguardian/world/rss': '//div[@class="flexible-content-body"]//text()',
 u'feed/https://portal.mytum.de/rssPresse': '//div[@id="news-content"]//text()',
 u'feed/http://www.guardian.co.uk/science/rss': '//div[@itemprop="articleBody"]//p//text()',
 u'feed/http://www.tomshardware.de/feeds/atom/all.xml': '//article[@id="news-content"]//p//text()',
 u'feed/http://vr-zone.com/feed': '//div[@id="content-area"]//p//text()',
 u'feed/http://thehouseofportable.blogspot.com/feeds/posts/default': None,
 u'feed/http://feeds.theinquirer.net/feed/vnunet/the_INQUIRER': '//div[@class="contenttop_text"]//p//text()',
 u'feed/http://www.hardwareboard.eu/external.php?do=rss&type=newcontent&sectionid=22&days=120&count=10': '//div[@class="entry-content"]//p//text()',
 u'feed/http://feeds.feedburner.com/RichardWisemansBlog?format=xml': '//div[@class="entry-content"]//p//text()',
 u'feed/https://portal.mytum.de/studium/preise/asRss': None,
 u'feed/https://portal.mytum.de/newsboards/news_students/asRss': '//div[@id="news-content"]//p//text()',
 u'feed/https://wiki.stusta.mhn.de/Spezial:Semantische_Suche/-5B-5BKategorie:News-5D-5D/-3FTitel/-3FDatum/-3FAutor/-3FZusammenfassung/-3FBild/order%3DDESC/sort%3DDatum/format%3Drss': None,
 u'feed/https://www.computerbase.de/rss/news.xml': '//div[@class="text-content"]//p//text()',
 u'feed/http://www.tagesschau.de/xml/rss2': '//div[@class="beitrag"]//p//text()',
 u'feed/http://www.heise.de/developer/rss/news-atom.xml': '//div[@class="meldung_wrapper"]//p//text()',
 u'feed/http://mpi.fs.tum.de/fsmpi/RSS': None,
 u'feed/https://www.in.tum.de/index.php?id=106&type=100': '//div[@class="news-shorttext"]//p//text()',
 u'feed/http://www.tv48erlangen-badminton.de/cms/?feed=rss2': '//div[@class="entry"]//p//text()',
 u'feed/http://www.heise.de/tp/news-atom.xml': '//div[@class="pos-content artext"]//p//text()',
 u'feed/http://portableapps.com/blog/2/feed': None,
 u'feed/http://www.anandtech.com/rss/': None,
 u'feed/http://www.test.de/rss/alles/': '//div[@id="primary"]//p//text()',
 u'feed/http://portableappz.blogspot.com/feeds/posts/default': None,
 u'feed/http://feeds2.feedburner.com/mydealz': '//div[@class="section-sub text--word-wrap"]//text()',
 u'feed/http://www.hardware-infos.com/rss/news.xml': '//div[@class="post"]//text()',
 u'feed/http://newsfeed.zeit.de/index': '//div[@class="article-body"]//p//text()',
 u'feed/http://www.engadget.com/rss.xml': '//div[@class="copy post-body"]//p//text()',
 u'feed/http://www.hardwareluxx.de/index.php/rss/feed/3.html': '//div[@itemprop="articleBody"]//text()',
 u'feed/https://www.computerbase.de/rss/artikel.xml': None,
 u'feed/http://feeds.gawker.com/lifehacker/full': '//div[@class="post-content entry-content  new-annotation"]//p//text()',
 u'feed/http://rss.golem.de/rss.php?feed=RSS2.0': '//div[@class="formatted"]//p//text()',
 u'feed/http://googleblog.blogspot.com/feeds/posts/default': None,
 u'feed/http://rivva.de/rss.xml': '//article//a/@href',
 u'feed/https://xkcd.com/rss.xml': '//div[@class=""]//p//text()',
 u'feed/http://static.winfuture.de/feeds/WinFuture-News-atom1.0.xml': '//div[@id="news_content"]/text()',
 u'feed/https://news.ycombinator.com/rss': None,
 u'feed/http://www.urlaubspiraten.de/feed': '//div[@class="sPost-ct editor"]//p//text()',
 u'feed/http://www.prad.de/feed_10.xml': '//span[@class="news-content"]/div/text()',
 u'feed/https://www.siemens.com/press/apps/PageRss/de/pressrelease.php?content[]=CC&content[]=E&content[]=ES&content[]=EH&content[]=EP&content[]=ET&content[]=EW&content[]=H&content[]=HAU&content[]=HCP&content[]=HCX&content[]=HDX&content[]=HIM&content[]=I&content[]=ICS&content[]=IDT&content[]=IIA&content[]=IMT&content[]=IC&content[]=ICBT&content[]=ICLMV&content[]=ICMOL&content[]=ICRL&content[]=ICSG': None,
 u'feed/http://www.manager-magazin.de/news/index.rss': '//div[@class="mmArticleColumnInner"]//p//text()',
 u'feed/http://rss.sueddeutsche.de/rss/Eilmeldungen': '//section[@class="body"]//p//text()',
 u'feed/http://suche.sueddeutsche.de/rss/Topthemen': '//section[@class="body"]//p//text()',
}

def get_rss_content(stream_id, link):
    if stream_id not in rss_mappings or not rss_mappings[stream_id]:
        return ""

    if hasattr(rss_mappings[stream_id], "__call__"):
        return rss_mappings[stream_id](link)
    else:
        return reduce(lambda x,y: x+y[0],Scraper.http_request(link, selectors=[Storage(xpath=rss_mappings[stream_id])]), "")