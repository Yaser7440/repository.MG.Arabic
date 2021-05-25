# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, re, traceback
from exoscrapers.modules import client, log_utils, cleantitle, source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.faselhd.pro']
        self.base_link = 'https://www.faselhd.pro'
		
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/search/%s+%s/feed/rss2/' % (mtitle, year)
            r = client.request(url)
            items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(r)
            for item in items:
                match = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>', re.DOTALL).findall(item)
                for row_title, row_url in match:
                    if cleantitle.get(title) in cleantitle.get(row_title):
                        if year in str(row_title):
                            return row_url
                        
            return url
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---FASELHD Testing - Exception: \n' + str(failure))
			return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s/feed/rss2/' % tvshowtitle
			r = client.request(url)
			items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(r)
			for item in items:
				match = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>', re.DOTALL).findall(item)
				for row_title, row_url in match:
					if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
						return row_url
			return
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---FASELHD Testing - Exception: \n' + str(failure))
			return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
			if not url:
				return
			log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			r = client.request(url)
			seasons = re.compile('id="seasonList">(.+?)<script', re.DOTALL).findall(r)
			for se in seasons:
				match = re.compile('data-href="(.+?)".+?class="title">(.+?)</div>', re.DOTALL).findall(se)
				for seasonid, row_season in match:
					if cleantitle.get(season) in cleantitle.get(row_season):
						url_season = self.base_link + "/?p=" + seasonid
			 			r = client.request(url_season)
						episodes = re.compile('id="epAll">(.+?)</div>', re.DOTALL).findall(r)
						for ep in episodes:
							match = re.compile('<a href="(.+?)"(.+?)</a>', re.DOTALL).findall(ep)
							for row_url, row_episode in match:
								if cleantitle.get(episode) in cleantitle.get(row_episode):
									return row_url

			return
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---FASELHD Testing - Exception: \n' + str(failure))
			return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = client.request(url)
            results = re.compile('player_iframe.+?=\s(?:\"|\')(.+?)(?:&img=|\')', re.DOTALL).findall(r)
            for url in results:
				url = client.replaceHTMLCodes(url.replace('%2F','/').replace('%3A',':').replace('%3F','?').replace('\r','').replace('\n',''))
				url = url.replace('https://www.faselhd.life/player/embed.php?url=','').replace('nv2=true&uid=0&','').replace('https://www.faselhd.live/player/embed.php?url=','')
				url = url.replace('faselhd.life','faselhd.pro')
				url = "https:" + url if not url.startswith('http') else url
				if 'faselhd' in url:
						try:
							result = client.request(url, headers=headers)
							match = re.compile('(?:file:)\s*(?:\"|\')(.+?)(?:\"|\')', re.DOTALL).findall(result)
							for link in match:
								link = link.replace('"','')
								link = "https:" + link if not link.startswith('http') else link
								# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
								log_utils.log('link = %s' % link, log_utils.LOGDEBUG)
								sources.append({'source': 'faseldom', 'quality': '1080p', 'language': 'ar', 'url': link,
												'direct': True, 'debridonly': False})
						except Exception:
							pass

				else:					

					
						valid, host = source_utils.is_host_valid(url, hostDict)
						if valid:
							if host in str(sources):
								continue
							quality, info = source_utils.get_release_quality(url, url)			
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': '', 
										'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---FASELHD Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url