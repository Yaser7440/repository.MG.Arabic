# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import traceback, re
from openscrapers.modules import client, cleantitle, log_utils, source_utils

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['w1.cima4u.io']
		self.base_link = 'http://w1.cima4u.io'
		self.episode_link = '/%s/'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
		

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s+%s/feed/rss2/' % (mtitle, year)
			r = client.request(url)
			items = re.compile('class="MovieBlock">(.+?)</a></li>', re.DOTALL).findall(r)
			for item in items:
				match = re.compile('<a href="(.+?)">.+?</i>.+?</div></div>(.+?)</div></div>').findall(item)
				for row_url, row_title in match:
					if cleantitle.get(title) in cleantitle.get(row_title):
						if year in str(row_title):
							return row_url			
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cima4u Testing - Exception: \n' + str(failure))
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s/feed/rss2/' % mtitle
			r = client.request(url)
			items = re.compile('class="MovieBlock">(.+?)</a></li>', re.DOTALL).findall(r)
			for item in items:
				match = re.compile('<a href="(.+?)">.+?</i>.+?</div></div>(.+?)</div></div>').findall(item)
				for row_url, row_title in match:
					if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
						#if year in str(row_title):
						return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cima4u Testing - Exception: \n' + str(failure))
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			r = client.request(url)
			results = re.compile('class="WatchNow">.+?href="(.+?html)"', re.DOTALL).findall(r)
			for link in results:
				r = client.request(link)
				seasons = re.compile('class="EpisodesSection">(.+?)</ul>', re.DOTALL).findall(r)
				for se in seasons:
					results = re.compile('<li class="EpisodeItem"><a href="(.+?html)"><em>حلقة</em><span>(.+?)</span></a></li>', re.DOTALL).findall(se)
					for row_url, row_episode in results:
						if cleantitle.get(episode) in cleantitle.get(row_episode):
							return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cima4u Testing - Exception: \n' + str(failure))
			return
			

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			hostDict = hostDict + hostprDict
			r = client.request(url)
			results = re.compile('class="WatchNow">.+?href="(.+?html)"', re.DOTALL).findall(r)
			for link in results:
				try:
					link = "https:" + link if not link.startswith('http') else link	
					r = client.request(link)
					data = re.compile('data-link="(.+?)"').findall(r)
					for video in data:
						video = 'http://live.cima4u.io/structure/server.php?id=%s' % video
						#log_utils.log('cima4u = %s' % video, log_utils.LOGDEBUG)
						r = client.request(video)
						results = re.compile('(?:iframe|source).+?(?:src)=(?:\"|\')(.+?)(?:\"|\')').findall(r)
						for url in results:
							valid, host = source_utils.is_host_valid(url, hostDict)
							quality, info = source_utils.get_release_quality(url, url)
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
											'direct': False, 'debridonly': False})
				except Exception:
					pass

			return sources
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---cima4u Testing - Exception: \n' + str(failure))
			return sources

	def resolve(self, url):	
		return url