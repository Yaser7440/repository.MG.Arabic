# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, traceback
from exoscrapers.modules import client, getSum, cleantitle, log_utils, source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['mycima.art']
        self.base_link = 'https://mycima.art'
		
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
			mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/AjaxCenter/Searching/%s+%s' % (mtitle, year)
			r = getSum.get(url)
			items = getSum.findEm(r, '{"output":"(.+?)"}')
			for item in items:
				item = getSum.replaceHTMLCodes(item)
				match = getSum.findEm(item,'GridItem"><a href="(.+?)" title="(.+?)">')
				for row_url, row_title in match:
					if cleantitle.get(title) in cleantitle.get(row_title):
						if year in str(row_title):
							return row_url
			return
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---MYCIMA Testing - Exception: \n' + str(failure))
			return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s/list/series/' % mtitle
			r = getSum.get(url, Type='cfscrape')
			items = getSum.findEm(r,'GridItem"><a href="(.+?)" title="(.+?)">')
			for row_url, row_title in items:
				if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
					#if year in str(row_title):
					return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---MYCIMA Testing - Exception: \n' + str(failure))
			return
			
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			r = getSum.get(url, Type='cfscrape')
			seasons = getSum.findEm(r, 'class="List--Seasons--Episodes">(.*?)</div>')
			for se in seasons:
				match = getSum.findEm(se,'href="(.+?)">(.+?)</a>')
				for url_season, row_season in match:
					if cleantitle.get(season) in cleantitle.get(row_season):
			 			r = getSum.get(url_season, Type='cfscrape')
						episodes = getSum.findEm(r, 'class="Episodes--Seasons--Episodes">(.*?)</div></div></div>')
						for ep in episodes:
							match = getSum.findEm(ep,'href="(.+?)".+?<episodeTitle>(.+?)</episodeTitle>')
							for row_url, row_episode in match:
								if cleantitle.get(episode) in cleantitle.get(row_episode):
									return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---MYCIMA Testing - Exception: \n' + str(failure))
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
            html = getSum.findall(r, '<ul class="WatchServersList">(.*?)</script></div><script>')#[0]
            for links in html:
					results = getSum.findall(links, '"(http.+?)"')
					for link in results:
						try:
							if 'uppom' in link:
								#log_utils.log('mycima = %s' % link , log_utils.LOGDEBUG)
								valid, host = source_utils.is_host_valid(link, hostDict)
								quality, info = source_utils.get_release_quality(link, link)
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link,
												'direct': True, 'debridonly': False})
							elif 'mycima.to' in link:
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
			log_utils.log('---MYCIMA Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url