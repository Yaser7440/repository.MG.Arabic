# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, re, traceback
from openscrapers.modules import client, log_utils, cleantitle, source_utils

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
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cimaclub Testing - Exception: \n' + str(failure))
			return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            r = client.request(url)
            results = re.compile('class="content-box">.+?href="(.+?)"', re.DOTALL).findall(r)
            for url in results:
				url = url.replace('film','watch')
				r = client.request(url)
				results = re.compile('(?:iframe|rel="nofollow).+?(?:src|href)=(?:\")(.+?)(?:\")', re.DOTALL).findall(r)
				for link in results:
					link = client.replaceHTMLCodes(link.replace('%2F','/').replace('%3A',':').replace('%3F','?').replace('\r','').replace('\n',''))
					link = link.replace('www.','').replace('https://cimaclub.one/?download=','').replace('https://cimaclub.cam/?download=','')
					link = "https:" + link if not link.startswith('http') else link
					if 'govid.me' in link:
						try:
							link = link.replace('embed-','')
							result = client.request(link)
							match = re.compile('file:"(.+?)",label:"(.+?)"', re.DOTALL).findall(result)
							for url, label in match:
								url = url.replace('"','')
								url = "https:" + url if not url.startswith('http') else url
								valid, host = source_utils.is_host_valid(link, hostDict)
								quality, info = source_utils.get_release_quality(label, label)
								url += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								#log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
								sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': url,
												'direct': True, 'debridonly': False})
						except Exception:
							pass
								
					# elif 'uppom' in link:
						# try:
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# quality, info = source_utils.get_release_quality(link, link)
							# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
							# sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link,
											# 'direct': True, 'debridonly': False})
						# except Exception:
							# pass
					else:					

					
						valid, host = source_utils.is_host_valid(link, hostDict)
						if valid:
							if host in str(sources):
								continue
							quality, info = source_utils.get_release_quality(link, link)			
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': '', 
										'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cimaclub Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url