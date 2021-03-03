# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib
from openscrapers.modules import client, log_utils, jsunpack, cleantitle, source_utils, getSum

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['land4movies.tv']
        self.base_link = 'https://land4movies.tv' 

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
			mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s+%s/feed/rss2/' % (mtitle, year)
			r = getSum.get(url)
			items = getSum.findEm(r, '<item>(.+?)</item>')
			for item in items:
				match = getSum.findEm(item,'<title>(.+?)</title>.+?<link>(.+?)</link>')
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
			links = getSum.get(url)
			videos = getSum.findEm(links, "(?:data-source|data-sourceX)\s*=(.+?) onclick")
			for video in videos:
				#log_utils.log('video = %s' % video, log_utils.LOGDEBUG)
				video = video.replace('"', '')
				video = video.replace('www.', '').replace('emb.html?', 'embed-').replace('=img.vup.to', '.html?auto=1&')
				video = video.replace('fembed', 'feurl').replace('/f/', '/v/').replace('supervideo.tv/e/', 'supervideo.tv/')
				
				if '7-up.net' in video:
					video = video.replace('net/','net/embed-') if 'embed' not in video else video
					r = getSum.get(video, Type='cfscrape')
					jc = getSum.findEm(r, 'sources:\s*\[.+?"file":"(.+?)"')
					for link in jc:
						#try:
							valid, host = source_utils.is_host_valid(link, hostDict)
							link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
							sources.append({'source': host, 'quality': 'HD', 'info': '', 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
						# except:
							# source_utils.scraper_error('land4movies')
							# pass
				# if 'youdbox' in video:
					# r = getSum.get(video, Type='cfscrape')
					# jc = getSum.findEm(r, 'source\s*src="(.+?)"')	
					# for link in jc:
						# #try:
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
							# sources.append({'source': host, 'quality': 'HD', 'info': '', 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
						# # except:
							# # source_utils.scraper_error('land4movies')
							# # pass
				# elif 'moshahda' in video:
					# # try:
						# r = getSum.get(video, Type='cfscrape')
						# data = getSum.findEm(r, r'\s*(eval.+?)\s*</script')[0]
						# r = jsunpack.unpack(data)
						# jc = getSum.findEm(r, 'file:(?:\"|\')(.+?)(?:\"|\'),label:(?:\"|\')(.+?)(?:\"|\')')
						# for link, label in jc:
							# quality, info = source_utils.get_release_quality(label, label)
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
							# sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': link, 'direct': True, 'debridonly': False})
					# # except:
						# # source_utils.scraper_error('land4movies')
						# # pass
				else:

				  try:
					valid, host = source_utils.is_host_valid(video, hostDict)
					if valid:
						if host in str(sources):
							continue
						#quality, info = source_utils.get_release_quality(video, video)
						sources.append({'source': host, 'quality': 'HD', 'language': 'ar', 'info': '', 'url': video, 'direct': False, 'debridonly': False})
				  except:
					source_utils.scraper_error('land4movies')
					pass



			return sources
		except:
			source_utils.scraper_error('land4movies')
			return sources

    def resolve(self, url):	
            return url