# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, re
from playscrapers.modules import client ,log_utils ,cleantitle ,source_utils

class source:	
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['faselhd.pro']
		self.base_link = 'https://www.faselhd.pro'
		self.episode_link = '/episodes/مسلسل-%s-الموسم-%s-الحلقه-%s'
		self.episode2_link = '/episodes/مسلسل-%s-الموسم-%s-الحلقة-%s'
		self.season_link = '/seasons/مسلسل-%s'

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
			source_utils.scraper_error('FASELHD')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			#url = cleantitle.geturl(tvshowtitle)
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search/%s/feed/rss2/' % tvshowtitle
			r = client.request(url)
			items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(r)
			for item in items:
				match = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>', re.DOTALL).findall(item)
				for row_title, row_url in match:
					if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
						#log_utils.log('tvshowfaseldom = %s' % cleantitle.get(tvshowtitle), log_utils.LOGDEBUG)
						return row_url
			return
		except:
			source_utils.scraper_error('FASELHD')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			#tvshowtitle = url
			#ep = '%01d' % int(episode)

			# url = urljoin(self.base_link, self.episode_link % (tvshowtitle, self.season_fixer(season), ep))
			# r = client.request(url)
			# items = re.compile('<title>(.*?)</title>', re.DOTALL).findall(r)
			# for item in items:
				# if cleantitle.get(tvshowtitle) not in cleantitle.get(item):
					# url = urljoin(self.base_link, self.episode2_link % (tvshowtitle, self.season_fixer(season), ep))
			#url = urljoin(self.base_link, self.season_link % (url))
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
		except:
			source_utils.scraper_error('FASELHD')
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			hostDict = hostDict + hostprDict
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
			r = client.request(url, headers=headers, XHR=True, timeout='10')
			results = re.compile('player_iframe.+?=\s(?:\"|\')(.+?)(?:&img=|\')', re.DOTALL).findall(r)
			for link in results:
				link = "https:" + link if not link.startswith('http') else link
				link = client.replaceHTMLCodes(link.replace('%3A', ':').replace('%2F', '/'))
				#link = link.replace('nv2=true&','').replace('uid=0&','').replace('&img','')
				link = link.replace('https://www.faselhd.life/player/embed.php?url=','').replace('nv2=true&uid=0&','').replace('https://www.faselhd.live/player/embed.php?url=','')
				#log_utils.log('link = %s' % link, log_utils.LOGDEBUG)
				if 'faselhd' in link:
					d = client.request(link, headers=headers)
					videos = re.compile('(?:file:)\s*(?:\"|\')(.+?)(?:\"|\')', re.DOTALL).findall(d)
					for video in videos:
						#valid, host = source_utils.is_host_valid(link, hostDict)
						#video = video.replace('https','http')
						#video = video.replace('index.m3u8','master.m3u8')
						video += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
						#log_utils.log('faseldom = %s' % video, log_utils.LOGDEBUG)
						sources.append({'source': 'faseldom', 'quality': '1080p', 'language': 'ar',
										'url': video, 'direct': True, 'debridonly': False})
						
				else:
					valid, host = source_utils.is_host_valid(link, hostDict)
					if valid:
						if host in str(sources): 
							continue
						sources.append({'source': host, 'quality': '1080p', 'language': 'ar',
										'url': link, 'direct': False, 'debridonly': False})

			return sources
		except:
			source_utils.scraper_error('FASELHD')
			return sources
	
	def season_fixer(self, season):
		if '1' in season:
			return 'الأول'
		elif '2' in season:
			return 'الثانى'
		elif '3' in season:
			return 'الثالث'
		elif '4' in season:
			return 'الرابع'
		elif '5' in season:
			return 'الخامس'
		elif '6' in season:
			return 'السادس'
		elif '7' in season:
			return 'السابع'
		elif '8' in season:
			return 'الثامن'
		elif '9' in season:
			return 'التاسع'
		elif '10' in season:
			return 'العاشر'
		elif '11' in season:
			return 'الحادي-عشر'
		elif '12' in season:
			return 'الثاني-عشر'
		elif '13' in season:
			return 'الثالث-عشر'
		elif '14' in season:
			return 'الرابع-عشر'
		elif '15' in season:
			return 'الخامس-عشر'			
		else:
			return 'الأخيرة'

	def resolve(self, url):	
		return url