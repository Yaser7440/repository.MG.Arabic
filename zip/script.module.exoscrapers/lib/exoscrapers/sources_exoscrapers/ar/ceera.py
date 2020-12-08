# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import traceback, re
from exoscrapers.modules import client, cleantitle, log_utils, source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watch.ceera.news']
		self.base_link = 'https://watch.ceera.news'
		self.episode_link = '/browse-watch-mosalsal-%s-video-season-%s-arabic-motarjam-videos-1-views.html'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvshowtitle = cleantitle.geturl(tvshowtitle)
			url = tvshowtitle
			return url
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ceera Testing - Exception: \n' + str(failure))
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			season_url = '%01d' % int(season)
			episode_url = 'episode-%01d' % int(episode)
			
			url = self.base_link + self.episode_link % (tvshowtitle, season_url)

			ep = client.request(url)
			results = re.compile('<a href="(.+?)"\s*title', re.DOTALL).findall(ep)
			for epi in results:
				if episode_url in epi and tvshowtitle in epi:
					return epi
			
			return url
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ceera Testing - Exception: \n' + str(failure))
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			hostDict = hostprDict + hostDict
			r = client.request(url)
			results = re.compile('<IFRAME\s*SRC="(.+?)".+?</IFRAME>', re.DOTALL).findall(r)
			for url in results:
				#log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

				try:
					if 'segavid' in url or 'vidsat' in url:
						d = client.request(url)
						videos = re.compile('''sources:\s*\[{file:\s*"(?P<url>[^"]+)''', re.DOTALL).findall(d)
						for video in videos:
							quality = source_utils.check_url(video)
							host = video.split('//')[1].replace('www.', '')
							host = host.split('/')[0].lower()
							video = video.replace('https','http')
							sources.append({'source': host, 'quality': quality, 'info': '', 'language': 'ar', 'url': video,
												'direct': True, 'debridonly': False})
						
					else:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if valid:
							if host in str(sources): 
								continue
							quality, info = source_utils.get_release_quality(url, url)
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
											'direct': False, 'debridonly': False})
							

				except Exception:
					pass

			return sources
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ceera Testing - Exception: \n' + str(failure))
			return sources

	def resolve(self, url):
		return url