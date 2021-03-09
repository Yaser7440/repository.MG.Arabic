# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
#from openscrapers.modules import log_utils


#import urllib
#from openscrapers.modules import client
from openscrapers.modules import cleantitle
from openscrapers.modules import source_utils
from openscrapers.modules import getSum

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watch.ceera.news']
		self.base_link = 'https://watch.ceera.news'
		self.episode_link = '/browse-watch-mosalsal-%s-video-season-%s-arabic-motarjam-videos-1-views.html'

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvshowtitle = cleantitle.geturl(tvshowtitle)
			url = tvshowtitle
			return url
		except:
			source_utils.scraper_error('ceera')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			season_url = '%01d' % int(season)
			episode_url = 'episode-%01d' % int(episode)
			
			url = self.base_link + self.episode_link % (tvshowtitle, season_url)

			ep = getSum.get(url)
			results = getSum.findEm(ep, '<a href="(.+?)"\s*title')
			for epi in results:
				if episode_url in epi and tvshowtitle in epi:
					return epi
			
			return url
		except:
			source_utils.scraper_error('ceera')
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			hostDict = hostprDict + hostDict

			r = getSum.get(url)
			results = getSum.findEm(r, '<IFRAME\s*SRC="(.+?html).+?</IFRAME>')
			for url in results:
				#log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
				# if any(x in url.lower() for x in ['vidsat.net']):
					# continue
				if 'segavid' in url or 'vidsat' in url:
					d = getSum.get(url)
					videos = getSum.findEm(d,'''sources:\s*\[{file:\s*"(?P<url>[^"]+)''')
					for video in videos:
						quality = source_utils.check_url(video)
						host = video.split('//')[1].replace('www.', '')
						host = host.split('/')[0].lower()
						video = video.replace('https','http')
						#log_utils.log('video = %s' % video, log_utils.LOGDEBUG)
						#video += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
						sources.append({'source': host, 'quality': quality, 'info': '', 'language': 'ar', 'url': video,
											'direct': True, 'debridonly': False})
						
				else:
					valid, host = source_utils.is_host_valid(url, hostDict)
					if valid:
						if host in str(sources): 
							continue
						quality, info = source_utils.get_release_quality(url, url)
						sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url, 'direct': False, 'debridonly': False})


			return sources
		except:
			source_utils.scraper_error('ceera')
			return sources

	def resolve(self, url):
		return url