# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.


#import re
#import requests
#from openscrapers.modules import log_utils
from openscrapers.modules import directstream
from openscrapers.modules import cleantitle
from openscrapers.modules import source_utils
from openscrapers.modules import getSum

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['w.egbest2.com']
        self.base_link = 'https://w.egbest2.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            title = cleantitle.geturl(title)
            url = self.base_link + '/wp-content/themes/YourColor/autoComplete.php?s=%s+%s' % (title, year)
            #log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
            return url
        except:
            source_utils.scraper_error('EGBEST2')
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict

            r = getSum.get(url, Type='cfscrape')
            #log_utils.log('links = %s' % r, log_utils.LOGDEBUG)
            results = getSum.findEm(r, '<a href="(.+?)"')
            for url in results:
				#log_utils.log('links = %s' % url, log_utils.LOGDEBUG)
				links = getSum.get(url, Type='cfscrape')
				videos = getSum.findEm(links, '(?:iframe|source).+?(?:src)=(?:\"|\')(.+?)(?:\"|\')')
				
				for url in videos:
					url = "https:" + url if not url.startswith('http') else url
					if any(x in url.lower() for x in ['gounlimited', 'youtube', 'vimeo']):
						continue
					elif 'vidshar' in url:
					
						result = getSum.get(url)
						match = getSum.get_sources(result)
						for link in match:
							link = link.replace('"','')
							link = "https:" + link if not link.startswith('http') else link
							#link = requests.get(link).url if 'jawcloud' in link else link
							valid, host = source_utils.is_host_valid(link, hostDict)
							#log_utils.log('vidshar link = %s' % link, log_utils.LOGDEBUG)
							if valid:
								quality, info = source_utils.get_release_quality(link, link)
								sources.append(
										{'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': link,
											'direct': False, 'debridonly': False})
					else:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if valid:
							#log_utils.log('vidshar url = %s' % url, log_utils.LOGDEBUG)
							quality, info = source_utils.get_release_quality(url, url)
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
											'direct': False, 'debridonly': False})
            return sources
        except:
            source_utils.scraper_error('EGBEST2')
            return sources

	def resolve(self, url):
		if "google" in url:
			return directstream.googlepass(url)
		elif 'jawcloud' in url:
			r = getSum.get(url)
			url = getSum.get_sources(r)
			return url
		else:
			return url