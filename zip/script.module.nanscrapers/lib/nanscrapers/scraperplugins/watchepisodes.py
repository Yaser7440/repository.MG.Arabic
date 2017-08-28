import re
import urllib
import requests
import urlparse
import xbmc
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper


class Watchepisodes(Scraper):
    domains = ['watch-episodes.co']
    name = "watchepisodes"

    def __init__(self):
        self.base_link = 'http://www.watchepisodeseries4.com/'
        self.search_link = '/home/search?q=%s'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            headers = {'User-Agent': random_agent(), "X-Requested-With": "XMLHttpRequest"}
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = clean_title(title)
            ep_id = int(episode)
            season_id = int(season)
            html = requests.get(query, headers=headers, timeout=30).json()
            results = html['series']
            for item in results:
                r_title = item['original_name'].encode('utf-8')
                r_link = item['seo_name'].encode('utf-8')
                if cleaned_title == clean_title(r_title):
                    r_page = self.base_link + "/" + r_link
                    # print("WATCHEPISODES r1", r_title,r_page)
                    r_html = BeautifulSoup(requests.get(r_page, headers=headers, timeout=30).content)
                    r = r_html.findAll('div', attrs={'class': re.compile('\s*el-item\s*')})
                    for container in r:
                        try:
                            r_href = container.findAll('a')[0]['href'].encode('utf-8')
                            r_season = container.findAll('div', attrs={"class": "season"})[0].text.encode('utf-8')
                            r_episode = container.findAll('div', attrs={"class": "episode"})[0].text.encode('utf-8')
                            # print("WATCHEPISODES r3", r_href,r_title)
                            episode_check = "[sS]%02d[eE]%02d" % (int(season), int(episode))
                            match = re.search(episode_check, r_href)
                            if match:
                                    # print("WATCHEPISODES PASSED EPISODE", r_href)
                                    return self.sources(replaceHTMLCodes(r_href))
                            else:
                                if "%02d" % int(season) in r_season and "%02d" % int(episode) in r_episode:
                                    return self.sources(replaceHTMLCodes(r_href))
                        except:
                            pass
        except:
            pass
        return []

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
            r = html.findAll('div', attrs={'class': 'site'})
            for container in r:
                r_url = container.findAll('a')[0]['data-actuallink'].encode('utf-8')
                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(r_url.strip().lower()).netloc)[0]
                host = replaceHTMLCodes(host)
                host = host.encode('utf-8')
                sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': r_url, 'direct': False})

        except:
            pass
        return sources
