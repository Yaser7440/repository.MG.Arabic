# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
#from exoscrapers.modules import log_utils


from exoscrapers.modules import getSum
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['w1.cima4u.io']
		self.base_link = 'http://w1.cima4u.io'
		self.episode_link = '/%s/'
		

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s+%s/feed/rss2/' % (mtitle, year)
			r = getSum.get(url)
			items = getSum.findEm(r, 'class="MovieBlock">(.+?)</a></li>')
			for item in items:
				match = getSum.findEm(item,'<a href="(.+?)">.+?</i>.+?</div></div>(.+?)</div></div>')
				for row_url, row_title in match:
					if cleantitle.get(title) in cleantitle.get(row_title):
						if year in str(row_title):
							return row_url
							# r = getSum.get(row_url)
							# results = getSum.findEm(r, 'class="WatchNow">.+?href="(.+?html)"')
							# for url in results:
								# url = "https:" + url if not url.startswith('http') else url
			
			return
		except:
			source_utils.scraper_error('cima4u')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s/feed/rss2/' % mtitle
			r = getSum.get(url)
			items = getSum.findEm(r, 'class="MovieBlock">(.+?)</a></li>')
			for item in items:
				match = getSum.findEm(item,'<a href="(.+?)">.+?</i>.+?</div></div>(.+?)</div></div>')
				for row_url, row_title in match:
					if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
						#if year in str(row_title):
						return row_url
			return
		except:
			source_utils.scraper_error('cima4u')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			r = getSum.get(url)
			results = getSum.findEm(r, 'class="WatchNow">.+?href="(.+?html)"')
			for link in results:
				r = getSum.get(link)
				seasons = getSum.findEm(r, 'class="EpisodesSection">(.+?)</ul>')
				for se in seasons:
					results = getSum.findEm(se, '<li class="EpisodeItem"><a href="(.+?html)"><em>حلقة</em><span>(.+?)</span></a></li>')
					for row_url, row_episode in results:
						if cleantitle.get(episode) in cleantitle.get(row_episode):
							return row_url
			return
		except:
			source_utils.scraper_error('cima4u')
			return
			

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			hostDict = hostDict + hostprDict
			r = getSum.get(url)
			results = getSum.findEm(r, 'class="WatchNow">.+?href="(.+?html)"')
			for link in results:
					link = "https:" + link if not link.startswith('http') else link	
					r = getSum.get(link)
					data = getSum.findEm(r, 'data-link="(.+?)"')
					for video in data:
						video = 'http://live.cima4u.io/structure/server.php?id=%s' % video
						#log_utils.log('cima4u = %s' % video, log_utils.LOGDEBUG)
						r = getSum.get(video)
						results = getSum.findSum(r)
						for url in results:
							valid, host = source_utils.is_host_valid(url, hostDict)
							quality, info = source_utils.get_release_quality(url, url)
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': '', 'url': url, 'direct': False, 'debridonly': False})
						


			return sources
		except:
			source_utils.scraper_error('cima4u')
			return sources

	def resolve(self, url):	
		return url