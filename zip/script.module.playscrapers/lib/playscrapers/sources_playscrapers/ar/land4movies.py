# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, traceback, re
from playscrapers.modules import client, jsunpack, cleantitle, log_utils, source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['land4movies.tv']
        self.base_link = 'https://land4movies.tv'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

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
			

			return
        except:
			source_utils.scraper_error('land4movies')
			return

    def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			hostDict = hostDict + hostprDict

            # r = getSum.get(url, Type='cfscrape')
            # results = getSum.findEm(r, 'class=movie-.+?href=(.+?) >')
            # for url in results:
			url = url + 'view/'
			links = client.request(url)
			videos = re.compile("(?:data-source|data-sourceX)\s*=(.+?) onclick", re.DOTALL).findall(links)
			for video in videos:
				try:
					video = video.replace('"', '')
					video = video.replace('www.', '').replace('emb.html?', 'embed-').replace('=img.vup.to', '.html?auto=1&')
					video = video.replace('fembed', 'feurl').replace('/f/', '/v/').replace('supervideo.tv/e/', 'supervideo.tv/')
				
					if '7-up.net' in video:
						try:
							video = video.replace('net/','net/embed-') if 'embed' not in video else video
							r = client.request(video, headers=self.headers)
							jc = re.compile('sources:\s*\[.+?"file":"(.+?)"', re.DOTALL).findall(r)
							for link in jc:
								valid, host = source_utils.is_host_valid(link, hostDict)
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
								sources.append({'source': host, 'quality': 'HD', 'info': '', 'language': 'ar', 'url': link,
												'direct': True, 'debridonly': False})
						except Exception:
							pass
					# if 'youdbox' in video:
						# r = getSum.get(video, Type='cfscrape')
						# jc = getSum.findEm(r, 'source\s*src="(.+?)"')	
						# for link in jc:
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
							# sources.append({'source': host, 'quality': 'HD', 'info': '', 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
						
					# elif 'moshahda' in video:
						# r = getSum.get(video, Type='cfscrape')
						# data = getSum.findEm(r, r'\s*(eval.+?)\s*</script')[0]
						# r = jsunpack.unpack(data)
						# jc = getSum.findEm(r, 'file:(?:\"|\')(.+?)(?:\"|\'),label:(?:\"|\')(.+?)(?:\"|\')')
						# for link, label in jc:
							# quality, info = source_utils.get_release_quality(label, label)
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
							# sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
					
					else:
						valid, host = source_utils.is_host_valid(video, hostDict)
						if valid:
							if host in str(sources):
								continue
							sources.append({'source': host, 'quality': 'HD', 'language': 'ar', 'url': video,
											'direct': False, 'debridonly': False})
				except Exception:
					pass



			return sources
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---land4movies Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url