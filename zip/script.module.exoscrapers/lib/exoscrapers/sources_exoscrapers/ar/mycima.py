# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib
import traceback
from exoscrapers.modules import client
from exoscrapers.modules import getSum
from exoscrapers.modules import cleantitle, log_utils
from exoscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['mycima.to']
        self.base_link = 'https://mycima.to'
		
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
			mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/AjaxCenter/Searching/%s+%s' % (mtitle, year)
			r = getSum.get(url)
			items = getSum.findEm(r, '{".*?":(.+?)"}]}')
			for item in items:
				match = getSum.findEm(item,'"url":"(.+?)","title":"(.+?)",')
				for row_url, row_title in match:
					row_url = getSum.replaceHTMLCodes(row_url)
					#log_utils.log('mycima = %s' % row_url , log_utils.LOGDEBUG)
					if cleantitle.get(title) in cleantitle.get(row_title):
						#if year in str(row_title):
							return row_url
			return
        except:
			source_utils.scraper_error('MYCIMA')
			return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            
            # r = getSum.get(url)
            # results = getSum.findall(r, 'class="BoxItem".+?href="(.+?)"')
            # for url in results:

            r = getSum.get(url, Type='client')
				
            html = getSum.findall(r, '<ul class="WatchServersList">(.*?)class="LeftFrontProfileSidebar">')#[0]
            for links in html:
					results = getSum.findall(links, 'href="(.+?)"')
					for link in results:
						try:
							if 'uppom' in link:
								#log_utils.log('mycima = %s' % link , log_utils.LOGDEBUG)
								valid, host = source_utils.is_host_valid(link, hostDict)
								quality, info = source_utils.get_release_quality(link, link)
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link,
												'direct': True, 'debridonly': False})
							elif 'mycima.io' in link:
								try:
									#log_utils.log('mycima = %s' % link , log_utils.LOGDEBUG)
									r = getSum.get(link)
									streams = getSum.findall(r, 'sources\:\s*\[(.+?)\]\,')[0]
									streams = getSum.findall(streams, 'format:\s*[\'"](.+?)[\'"].+?src:\s*[\'"](.+?)[\'"]')
									for label, link in streams:
										quality = source_utils.get_release_quality(label, label)[0]
										link += '|User-Agent=%s&Referer=%s' % (urllib.quote(client.agent()), link)
										sources.append({'source': 'mycima', 'quality': quality, 'info': '', 'language': 'ar', 'url': link,
														'direct': True, 'debridonly': False})
								except Exception:
									pass
							else:
								link = link
								#log_utils.log('link = %s' % link , log_utils.LOGDEBUG)
								valid, host = source_utils.is_host_valid(link, hostDict)
								if valid:
									quality, info = source_utils.get_release_quality(link, link)
									sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info,
													'url': link, 'direct': False, 'debridonly': False})
						except Exception:
							pass
            return sources
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---WATCHSERIESHD Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url