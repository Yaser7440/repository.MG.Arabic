# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
#from exoscrapers.modules import log_utils

#import urllib
#from exoscrapers.modules import client
from exoscrapers.modules import getSum
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cimaclub.me']
        self.base_link = 'https://www.cimaclub.me'
		
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/search?s=%s+%s' % (mtitle, year)
            #log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
            return url
        except:
            source_utils.scraper_error('cimaclub')
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict

            r = getSum.get(url)
            results = getSum.findEm(r, 'class="MovieBlock".+?href="(.+?)"')
            for url in results:
				#url = url + 'watch'
				
				r = getSum.get(url)
				results = getSum.findEm(r, '(?:class="Hoverable").+?(?:data-url|href)=(?:\")(.+?)(?:\")')
				for link in results:
					link = getSum.replaceHTMLCodes(link)
					link = link.replace('%2F','/').replace('%3A',':').replace('%3F','?').replace('www.','').replace('https://cimaclub.one/?download=','').replace('https://cimaclub.cam/?download=','')
					link = "https:" + link if not link.startswith('http') else link
					# if 'uppom' in link:
						# log_utils.log('url = %s' % link, log_utils.LOGDEBUG)
						# valid, host = source_utils.is_host_valid(link, hostDict)
						# quality, info = source_utils.get_release_quality(link, link)
						# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
						# sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link,
										# 'direct': True, 'debridonly': False})
					# else:					

					
					valid, host = source_utils.is_host_valid(link, hostDict)
					if valid:
						if host in str(sources):
							continue
						quality, info = source_utils.get_release_quality(link, link)			
						sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': '', 'url': link, 'direct': False, 'debridonly': False})
						

								





            return sources
        except:
            source_utils.scraper_error('cimaclub')
            return sources

    def resolve(self, url):	
            return url