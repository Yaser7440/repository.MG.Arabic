# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import requests
import re
from exoscrapers.modules import log_utils
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
            for url in match:
                host = url
            i = self.session.get(host, headers=self.headers).content			
            match = re.compile('<iframe name="player_iframe" src="(.+?)&img', flags=re.DOTALL | re.IGNORECASE).findall(i)
            for link in match:
                link = link.replace('nv2=true&','').replace('uid=0&','')
            d = self.session.get(link, headers=self.headers).content			
            match = re.compile('file: "(.+?)",', flags=re.DOTALL | re.IGNORECASE).findall(d)
            for vid in match:
                vid = vid				
                #log_utils.log('url2 = %s' % vid, log_utils.LOGDEBUG)
                valid, host = source_utils.is_host_valid(vid, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(vid, vid)

                    sources.append({'source': host, 'quality': '1080p', 'language': 'ar', 'info': info, 'url': vid, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources
    def resolve(self, url):	
        try:
            return url
        except:
            return