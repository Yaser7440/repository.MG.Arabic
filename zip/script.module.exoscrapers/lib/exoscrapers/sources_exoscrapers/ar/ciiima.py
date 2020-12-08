# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

try: from urlparse import urljoin
except ImportError: from urllib.parse import urljoin
import urllib, traceback, re
from exoscrapers.modules import client, cleantitle, log_utils, source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['tv.ciiima.com']
		self.base_link = 'http://tv.ciiima.com'
		self.movie_link = '/movie/%s-%s'
		self.episode_link = '/show/%s/season-%s/episode-%s'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + self.movie_link % (title, year)
			return url
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ciiima Testing - Exception: \n' + str(failure))
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvshowtitle = cleantitle.geturl(tvshowtitle)
			url = ('%s-%s') % (tvshowtitle, year)
			return url
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ciiima Testing - Exception: \n' + str(failure))
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			url = urljoin(self.base_link, self.episode_link % (tvshowtitle, season, episode))
			return url
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ciiima Testing - Exception: \n' + str(failure))
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			hostDict = hostprDict + hostDict
			#log_utils.log('episode = %s' % url, log_utils.LOGDEBUG)
			r = client.request(url, headers=self.headers)
			if 'show' in url:
				results = re.compile('Embedded=\s*(.+?)}];', re.DOTALL).findall(r)
			else:
				results = re.compile('Embedded:\s*(.+?)}],Type', re.DOTALL).findall(r)
			for result in results:
				results = re.compile('"(htt.+?)(?:\"|&id)', re.DOTALL).findall(result)
				for url in results:
					try:
						url = url.replace('\u002F','/').replace('www.','')
						url = "https:" + url if not url.startswith('http') else url
						if any(x in url.lower() for x in ['youtube']):
							continue
						#log_utils.log('links = %s' % url, log_utils.LOGDEBUG)
						if 'govid.me' in url:
							try:
								url = url.replace('embed-','')
								result = client.request(url)
								match = re.compile('sources\s*:\s*\[(.+?)\]').findall(result)
								for link in match:
									link = link.replace('"','')
									link = "https:" + link if not link.startswith('http') else link
									valid, host = source_utils.is_host_valid(url, hostDict)
									quality, info = source_utils.get_release_quality(url, url)
									link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
									sources.append({'source': host, 'quality': '720p', 'info': info, 'language': 'ar', 'url': link,
													'direct': True, 'debridonly': False})
							except Exception:
								pass
					
						elif 'uppom' in url:
							try:
								valid, host = source_utils.is_host_valid(url, hostDict)
								quality, info = source_utils.get_release_quality(url, url)
								url += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
								sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
												'direct': True, 'debridonly': False})
							except Exception:
								pass
						else:
							valid, host = source_utils.is_host_valid(url, hostDict)
							if valid:
								quality, info = source_utils.get_release_quality(url, url)
								sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
												'direct': False, 'debridonly': False})
					except Exception:
						pass
			return sources
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---ciiima Testing - Exception: \n' + str(failure))
			return sources

	def resolve(self, url):
		if 'jawcloud' in url:
			r = client.request(url)
			url = re.compile('sources\s*:\s*\[(.+?)\]').findall(r)
		elif 'vidshar' in url:
			r = client.request(url)
			url = re.compile('sources\s*:\s*\[(.+?)\]').findall(r)
			return url
		else:
			return url