# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, traceback, re
from exoscrapers.modules import client, cleantitle, log_utils, source_utils

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
			r = client.request(url)
			items = re.compile('{"output":"(.*?)"}', re.DOTALL).findall(r)
			for item in items:
				item = client.replaceHTMLCodes(item.replace("\/", "/").replace("\\", ""))
				match = re.compile('GridItem"><a href="(.+?)" title="(.+?)">', re.DOTALL).findall(item)
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
			r = client.request(url)
			items = re.compile('GridItem"><a href="(.+?)" title="(.+?)">', re.DOTALL).findall(r)
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
			r = client.request(url)
			seasons = re.compile('class="List--Seasons--Episodes">(.*?)</div>', re.DOTALL).findall(r)
			for se in seasons:
				match = re.compile('href="(.+?)">(.+?)</a>', re.DOTALL).findall(se)
				for url_season, row_season in match:
					if cleantitle.get(season) in cleantitle.get(row_season):
			 			r = client.request(url_season)
						episodes = re.compile('class="Episodes--Seasons--Episodes">(.*?)</div></div></div>', re.DOTALL).findall(r)
						for ep in episodes:
							match = re.compile('href="(.+?)".+?<episodeTitle>(.+?)</episodeTitle>', re.DOTALL).findall(ep)
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
            r = client.request(url)
            html = re.compile('class="WatchServersList">(.*?)</i></a></li></ul>', re.DOTALL).findall(r)
            for links in html:
					results = re.compile('"(http.+?)"', re.DOTALL).findall(links)
					for link in results:
						try:
							if 'uppom' in link:
								#log_utils.log('mycima = %s' % link , log_utils.LOGDEBUG)
								valid, host = source_utils.is_host_valid(link, hostDict)
								quality, info = source_utils.get_release_quality(link, link)
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link,
												'direct': True, 'debridonly': False})
							elif 'mycima.art' in link:
								try:
									#log_utils.log('mycima = %s' % link , log_utils.LOGDEBUG)
									r = client.request(link)
									streams = re.compile('sources\:\s*\[(.+?)\]\,', re.DOTALL).findall(r)[0]
									streams = re.compile('format:\s*[\'"](.+?)[\'"].+?src:\s*[\'"](.+?)[\'"]', re.DOTALL).findall(streams)
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