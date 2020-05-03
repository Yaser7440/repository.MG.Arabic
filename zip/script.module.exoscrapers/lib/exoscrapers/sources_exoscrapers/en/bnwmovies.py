# -*- coding: utf-8 -*-

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

import re

from exoscrapers.modules import cleantitle
from exoscrapers.modules import client

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['bnwmovies.com']
		self.base_link = 'http://www.bnwmovies.com'
		self.search_link = '/?s=%s'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			scrape = title.lower().replace(' ', '+').replace(':', '')
			start_url = self.base_link + self.search_link % scrape
			html = client.request(start_url)
			results = re.compile('href="(.+?)"', re.DOTALL).findall(html)
			for url in results:
				if self.base_link in url:
					if 'webcache' in url:
						continue
					if cleantitle.geturl(title) in url:
						chkhtml = client.request(url)
						chktitle = re.compile('<title.+?>(.+?)</title>', re.DOTALL).findall(chkhtml)[0]
						if title in chktitle:
							if str(year) in chktitle:
								return url
			return
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			html = client.request(url)
			Links = re.compile('<source.+?src="(.+?)"', re.DOTALL).findall(html)
			for link in Links:
				sources.append({'source': 'BNW', 'quality': 'SD', 'language': 'en', 'url': link, 'direct': True,
				                'debridonly': False})
			return sources
		except:
			return sources

	def resolve(self, url):
		return url
