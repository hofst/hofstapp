__author__ = 'Basti'
from Scraper import Scraper
from gluon.storage import Storage

rss_mappings = {
 u'feed/http://www.thenakedscientists.com/naked_scientists_podcast.xml': '//p[@class="bodytext"]//text()',
 u'feed/http://feeds.feedburner.com/ClPlBl': lambda link: "",
 u'feed/http://www.heise.de/newsticker/heise-atom.xml': '//div[@class="meldung_wrapper"]/p//text()',
 u'feed/http://dzone.com/mz/agile/rss': lambda link: "",
 u'feed/http://de.engadget.com/rss.xml': lambda link: "",
 u'feed/http://feeds.guardian.co.uk/theguardian/world/rss': lambda link: "",
 u'feed/https://portal.mytum.de/rssPresse': lambda link: "",
 u'feed/http://www.guardian.co.uk/science/rss': lambda link: "",
 u'feed/https://www.test.de/rss/themen/alle/alles/': lambda link: "",
 u'feed/http://feeds.pheedo.com/toms_hardware': lambda link: "",
 u'feed/http://www.vr-zone.com/rss.php': lambda link: "",
 u'feed/http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=mysteryxyx': lambda link: "",
 u'feed/http://thehouseofportable.blogspot.com/feeds/posts/default': lambda link: "",
 u'feed/http://feeds.theinquirer.net/feed/vnunet/the_INQUIRER': lambda link: "",
 u'feed/http://www.hardwareboard.eu/external.php?do=rss&type=newcontent&sectionid=22&days=120&count=10': lambda link: "",
 u'feed/http://feeds.feedburner.com/RichardWisemansBlog?format=xml': lambda link: "",
 u'feed/https://portal.mytum.de/studium/preise/asRss': lambda link: "",
 u'feed/https://portal.mytum.de/newsboards/news_students/asRss': lambda link: "",
 u'feed/https://wiki.stusta.mhn.de/Spezial:Semantische_Suche/-5B-5BKategorie:News-5D-5D/-3FTitel/-3FDatum/-3FAutor/-3FZusammenfassung/-3FBild/order%3DDESC/sort%3DDatum/format%3Drss': lambda link: "",
 u'feed/https://www.computerbase.de/rss/news.xml': lambda link: "",
 u'feed/http://www.tagesschau.de/xml/rss2': lambda link: "",
 u'feed/http://www.heise.de/developer/rss/news-atom.xml': lambda link: "",
 u'feed/http://mpi.fs.tum.de/fsmpi/RSS': lambda link: "",
 u'feed/https://www.in.tum.de/index.php?id=106&type=100': lambda link: "",
 u'feed/http://www.semesterticket-muenchen.de/blog/feed/': lambda link: "",
 u'feed/http://www.tv48erlangen-badminton.de/cms/?feed=rss2': lambda link: "",
 u'feed/http://www.heise.de/tp/news-atom.xml': lambda link: "",
 u'feed/http://portableapps.com/blog/2/feed': lambda link: "",
 u'feed/http://www.anandtech.com/rss/': lambda link: "",
 u'feed/http://www.heise.de/ct-tv/rss/news-atom.xml': lambda link: "",
 u'feed/http://www.test.de/rss/alles/': lambda link: "",
 u'feed/http://portableappz.blogspot.com/feeds/posts/default': lambda link: "",
 u'feed/http://feeds2.feedburner.com/mydealz': lambda link: '//div[@class="section-sub text--word-wrap"]//text()',
 u'feed/http://www.hardware-infos.com/rss/news.xml': lambda link: "",
 u'feed/http://newsfeed.zeit.de/index': lambda link: "",
 u'feed/http://www.engadget.com/rss.xml': lambda link: "",
 u'feed/http://support.lenovo.com/de_DE/rss/default.page?PROD=P014-S003-SS1009--': lambda link: "",
 u'feed/http://www.hardwareluxx.de/index.php/rss/feed/3.html': lambda link: "",
 u'feed/https://www.computerbase.de/rss/artikel.xml': lambda link: "",
 u'feed/http://feeds.gawker.com/lifehacker/full': lambda link: "",
 u'feed/http://feeds.pheedo.com/toms_hardware_headlines': lambda link: "",
 u'feed/http://rss.golem.de/rss.php?feed=RSS2.0': lambda link: "",
 u'feed/http://googleblog.blogspot.com/feeds/posts/default': lambda link: "",
 u'feed/https://twitter.com/statuses/user_timeline/58708041.rss': lambda link: "",
 u'feed/http://rivva.de/rss.xml': lambda link: "",
 u'feed/https://xkcd.com/rss.xml': lambda link: "",
 u'feed/http://static.winfuture.de/feeds/WinFuture-News-atom1.0.xml': lambda link: "",
 u'feed/https://news.ycombinator.com/rss': lambda link: "",
 u'feed/http://www.urlaubspiraten.de/feed': lambda link: "",
 u'feed/http://www.prad.de/feed_10.xml': lambda link: "",
 u'feed/https://www.siemens.com/press/apps/PageRss/de/pressrelease.php?content[]=CC&content[]=E&content[]=ES&content[]=EH&content[]=EP&content[]=ET&content[]=EW&content[]=H&content[]=HAU&content[]=HCP&content[]=HCX&content[]=HDX&content[]=HIM&content[]=I&content[]=ICS&content[]=IDT&content[]=IIA&content[]=IMT&content[]=IC&content[]=ICBT&content[]=ICLMV&content[]=ICMOL&content[]=ICRL&content[]=ICSG': lambda link: "",
 u'feed/http://www.manager-magazin.de/news/index.rss': lambda link: "",
 u'feed/http://rss.sueddeutsche.de/rss/Eilmeldungen': lambda link: "",
 u'feed/http://suche.sueddeutsche.de/rss/Topthemen': '//section[@class="body"]/p//text()',
}

def get_rss_content(stream_id, link):
    if stream_id not in rss_mappings:
        return ""

    if hasattr(rss_mappings[stream_id], "__call__"):
        return rss_mappings[stream_id](link)
    else:
        return reduce(lambda x,y: x+y[0],Scraper.http_request(link, selectors=[Storage(xpath=rss_mappings[stream_id])]), "")