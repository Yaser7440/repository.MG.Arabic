# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import requests
import re
#from exoscrapers.modules import log_utils
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils
#log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['faselhd.to']
        self.base_link = 'https://www.faselhd.to'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}
        self.session = requests.Session()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/?s=%s+%s' % (mtitle, year)
            #log_utils.log('url = %s' % url, log_utils.LOGDEBUG)			
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            r = self.session.get(url, headers=self.headers).content
            match = re.compile('class="movie-wrap".+?href="(.+?)"', flags=re.DOTALL | re.IGNORECASE).findall(r)
            for search_url in match:
                search_url = search_url
            i = self.session.get(search_url, headers=self.headers).content			
            #match = re.compile('<iframe name="player_iframe" src="(.+?)&img', flags=re.DOTALL | re.IGNORECASE).findall(i)
            match = re.compile('''player_iframe.location.href =\s*["']([^'"]+(?:&img|html))''', re.DOTALL | re.IGNORECASE).findall(i)
            for link in match:
                link = link.replace('nv2=true&','').replace('uid=0&','').replace('&img','')
                d = self.session.get(link, headers=self.headers).content
                # if 'video_player' in link:
				   # match = re.compile('''(?:src|file)(?:=|:)\s*["']([^'"]+m3u8)''').findall(d)
                #else:
                match = self.session.get(link, headers=self.headers).content
                match = re.compile('''(?:src|SRC|href|HREF|file)(?:=|:)\s*["']([^'"]+)''').findall(d)
                for links in match:
				   #log_utils.log('url2 = %s' % links, log_utils.LOGDEBUG)
				   links = links#.decode('utf-8')
				   if any(x in links.lower() for x in ['gounlimited', 'youtube']):
							continue
				   valid, host = source_utils.is_host_valid(links, hostDict)
				   if valid:
						if host in str(sources):
							continue
						quality, info = source_utils.get_release_quality(links, links)

						sources.append({'source': host, 'quality': '1080p', 'language': 'ar', 'info': info, 'url': links, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):	
            return url
