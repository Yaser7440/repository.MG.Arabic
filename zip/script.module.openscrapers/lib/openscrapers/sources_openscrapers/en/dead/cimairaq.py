# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
#from openscrapers.modules import log_utils
import urllib
from openscrapers.modules import client
from openscrapers.modules import getSum
from openscrapers.modules import cleantitle
from openscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cimairaq.com']
        self.base_link = 'https://cimairaq.com'
		
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/?s=%s+%s' % (mtitle, year)
            #log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
            return url
        except:
            source_utils.scraper_error('cimairaq')
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            #server = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            r = getSum.get(url)
            results = getSum.findEm(r, 'class="movie".+?href="(.+?)"')
            for url in results:
				url = url + '?view=1'
				r = getSum.get(url)
				id = getSum.findEm(r, "data:\s*'q=(.+?)'")[0]
				server = getSum.findEm(r, 'data-server="(.+?)')#[0]
				for i in server:
					video = 'https://cimairaq.com/wp-content/themes/AQEEL/servers/server.php?q=%s&i=%s' % (id, str(i))
					#log_utils.log('cimairaq = %s' % video, log_utils.LOGDEBUG)
					r = getSum.get(video)
					results = getSum.findSum(r)
					for url in results:
						url = url
					if 'moshahda' in url or 'gounlimited' in url:
							try:
								r = getSum.unpacked(url)
								jc = getSum.findEm(r, '(http.+?(?:m3u8|mp4))')
								for link in jc:
									quality, info = source_utils.get_release_quality(link, link)
									valid, host = source_utils.is_host_valid(link, hostDict)
									if valid:
										link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
										sources.append({'source': 'direct', 'quality': quality, 'info': '', 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
							except:
								source_utils.scraper_error('cimairaq')
								pass

					else:
							try:
								valid, host = source_utils.is_host_valid(url, hostDict)
								if valid:
									if host in str(sources):
										continue
									quality, info = source_utils.get_release_quality(url, url)
									sources.append({'source': host, 'quality': 'HD', 'language': 'ar', 'info': '', 'url': url, 'direct': False, 'debridonly': False})
							except:
								source_utils.scraper_error('cimairaq')
								pass
            return sources
        except:
            source_utils.scraper_error('cimairaq')
            return sources

    def resolve(self, url):	
            return url