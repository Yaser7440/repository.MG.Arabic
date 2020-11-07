# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib
from exoscrapers.modules import client
#from exoscrapers.modules import log_utils
from exoscrapers.modules import jsunpack
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils
from exoscrapers.modules import getSum

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['shahid4u.cam']
        self.base_link = 'https://shahid4u.cam'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/search?s=%s+%s' % (mtitle, year)
            #log_utils.log('search = %s' % url, log_utils.LOGDEBUG)
            return url
        except:
            source_utils.scraper_error('SHAHID4U')
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict

            r = getSum.get(url, Type='cfscrape')
            results = getSum.findEm(r, 'class="content-box".+?href="(.+?)"')
            for url in results:
				url = url.replace('film','watch')
				
				r = getSum.get(url)
				results = getSum.findSum(r)
				for link in results:
					
					link = link.replace(' ','').replace('https:', '').replace('\r', '')
					link = "https:" + link if not link.startswith('http') else link
					if 'vidhd' in link:
							# loc = re.findall('''https://vidhd.net/embed-(.+?)\r.html''', link, re.DOTALL)[0]
							# link = 'https://vidhd.net/embed-{0}.html'.format(loc)
						
							data = getSum.get(link)
							data = getSum.findEm(data, r'\s*(eval.+?)\s*</script')[0]
							link = jsunpack.unpack(data)
						 	jc = getSum.findEm(link, 'file:"(.+?)",label:"(.+?)"')
						 	for link, label in jc:
								#log_utils.log('url = %s' % link, log_utils.LOGDEBUG)
								quality, info = source_utils.get_release_quality(label, label)#[0]
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								#log_utils.log('link = %s' % link, log_utils.LOGDEBUG)
							
								sources.append(
									{'source': 'vidhd', 'quality': quality, 'language': 'ar', 'url': link, 'info': info,
									 'direct': True, 'debridonly': False})
					else:
						valid, host = source_utils.is_host_valid(link, hostDict)
						if not valid: continue
						sources.append(
							{'source': host, 'quality': 'SD', 'language': 'ar', 'url': link, 'info': '',
							 'direct': False, 'debridonly': False})

            return sources
        except:
            source_utils.scraper_error('SHAHID4U')
            return sources

	def resolve(self, url):
		return url