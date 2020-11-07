# -*- coding: UTF-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    exoscrapers Project
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

try: from urlparse import urljoin
except ImportError: from urllib.parse import urljoin
import urllib
from exoscrapers.modules import client
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils
#from exoscrapers.modules import log_utils
from exoscrapers.modules import getSum

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
		except:
			source_utils.scraper_error('ciiima')
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvshowtitle = cleantitle.geturl(tvshowtitle)
			url = ('%s-%s') % (tvshowtitle, year)
			return url
		except:
			source_utils.scraper_error('ciiima')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			url = urljoin(self.base_link, self.episode_link % (tvshowtitle, season, episode))
			return url
		except:
			source_utils.scraper_error('ciiima')
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			hostDict = hostprDict + hostDict
			#log_utils.log('episode = %s' % url, log_utils.LOGDEBUG)
			r = getSum.get(url, Type='cfscrape')
			if 'show' in url:
				results = getSum.findEm(r, 'Embedded=\s*(.+?)}];')
			else:
				results = getSum.findEm(r, 'Embedded:\s*(.+?)}],Type')
			for result in results:
				results = getSum.findEm(result, '"(htt.+?)(?:\"|&id)')
				for url in results:	
					url = url.replace('\u002F','/').replace('www.','')
					url = "https:" + url if not url.startswith('http') else url
					if any(x in url.lower() for x in ['youtube']):
						continue
					#log_utils.log('episode = %s' % url, log_utils.LOGDEBUG)
					if 'govid.me' in url:
						url = url.replace('embed-','')
						result = getSum.get(url)
						match = getSum.get_sources(result)
						for link in match:
							link = link.replace('"','')
							link = "https:" + link if not link.startswith('http') else link
							valid, host = source_utils.is_host_valid(url, hostDict)
							quality, info = source_utils.get_release_quality(url, url)
							link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
							sources.append({'source': host, 'quality': '720p', 'info': info, 'language': 'ar', 'url': link,
											'direct': True, 'debridonly': False})
						
					
					if 'uppom' in url:
						valid, host = source_utils.is_host_valid(url, hostDict)
						quality, info = source_utils.get_release_quality(url, url)
						url += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), url)
						sources.append({'source': host, 'quality': quality, 'info': info, 'language': 'ar', 'url': url,
										'direct': True, 'debridonly': False})
					# elif 'vidshar' in url:
						# result = getSum.get(url, Type='cfscrape')
						# match = getSum.get_sources(result)
						# for link in match:
							# link = link.replace('"','')
							# link = "https:" + link if not link.startswith('http') else link
							# valid, host = source_utils.is_host_valid(link, hostDict)
							# if valid:
								# quality, info = source_utils.get_release_quality(link, link)
								# sources.append(
										# {'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': link,
											# 'direct': False, 'debridonly': False})
					else:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if valid:
							quality, info = source_utils.get_release_quality(url, url)
							sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': url,
											'direct': False, 'debridonly': False})
			return sources
		except:
			source_utils.scraper_error('ciiima')
			return sources

	def resolve(self, url):
		if "google" in url:
			return directstream.googlepass(url)
		elif 'jawcloud' in url:
			r = getSum.get(url)
			url = getSum.get_sources(r)
		elif 'vidshar' in url:
			r = getSum.get(url)
			url = getSum.get_sources(r)
			return url
		else:
			return url