# -*- coding: utf-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # Muad'Dib wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

import re

from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import log_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.bnwmovies.com']
        self.base_link = 'https://bnwmovies.com'
        #self.search_link = '%s/search?q=bnwmovies.com+%s+%s'
        #self.goog = 'https://www.google.co.uk'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            scrape = title.lower().replace(' ','+')

            #start_url = self.search_link %(self.goog,scrape,year)
            start_url = self.base_link + self.search_link % scrape

            html = client.request(start_url)
            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
            for url in results:
                if self.base_link in url:
                    if 'webcache' in url:
                        continue
                    if cleantitle.geturl(title) in url:
                        chkhtml = client.request(url)
                        chktitle = re.compile('<title.+?>(.+?)</title>',re.DOTALL).findall(chkhtml)[0]
                        if title in chktitle:
                            if str(year) in chktitle:
                                return url
            return
        except:
            log_utils.log('BNWMovies - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            html = client.request(url)

            links = re.compile('<source.+?src="(.+?)"',re.DOTALL).findall(html)
            for link in links:
                sources.append({'source': 'direct', 'quality': 'SD', 'language': 'en', 'url': link, 'info': '', 'direct': True, 'debridonly': False})
            return sources
        except:
            log_utils.log('BNWMovies - Exception', 1)
            return sources

    def resolve(self, url):
        return url