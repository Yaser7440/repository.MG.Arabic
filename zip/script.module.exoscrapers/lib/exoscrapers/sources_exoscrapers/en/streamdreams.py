# -*- coding: UTF-8 -*-
# modified by Venom for Openscrapers (4-20-2020)
# Created by Tempest

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    ExoScrapers Project
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

from exoscrapers.modules import cfscrape
from exoscrapers.modules import cleantitle
from exoscrapers.modules import client
from exoscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['streamdreams.org']
		self.base_link = 'https://streamdreams.org'
		self.search_movie = '/movies/nnn-%s/'
		self.search_tv = '/shows/nnn-%s/'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			mvtitle = cleantitle.geturl(title)
			url = self.base_link + self.search_movie % mvtitle
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvtitle = cleantitle.geturl(tvshowtitle)
			url = self.base_link + self.search_tv % tvtitle
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			url = url + '?session=%s&episode=%s' % (season, episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			scraper = cfscrape.create_scraper()

			if url is None:
				return sources

			hostDict = hostprDict + hostDict
			headers = {'Referer': url}

			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			r = scraper.get(url).content
			if r is None:
				return sources

			u = client.parseDOM(r, "span", attrs={"class": "movie_version_link"})
			for t in u:
				match = client.parseDOM(t, 'a', ret='data-href')
				for url in match:
					if url in str(sources):
						continue
					valid, host = source_utils.is_host_valid(url, hostDict)
					if valid:
						quality, info = source_utils.get_release_quality(url, url)
						sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
			return sources
		except:
			source_utils.scraper_error('STREAMDREAMS')
			return sources

	def resolve(self, url):
		return url