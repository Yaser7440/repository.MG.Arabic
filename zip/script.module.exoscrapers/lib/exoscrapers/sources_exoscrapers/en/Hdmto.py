# -*- coding: UTF-8 -*-

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
from exoscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['hdm.to']
		self.base_link = 'https://hdm.to'
		self.search_link = '/search/%s+%s'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			t = cleantitle.geturl(title).replace('-', '+').replace('++', '+')
			url = self.base_link + self.search_link % (t, year)
			r = client.request(url)
			u = client.parseDOM(r, "div", attrs={"class": "col-md-2 col-sm-2 mrgb"})
			for i in u:
				link = re.compile('<a href="(.+?)"').findall(i)
				for url in link:
					if not cleantitle.get(title) in cleantitle.get(url):
						continue
					return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			hostDict = hostDict + hostprDict

			if url is None:
				return sources

			t = client.request(url)
			r = re.compile('<iframe.+?src="(.+?)"').findall(t)

			for url in r:
				url = url.replace(" ", "+")
				valid, host = source_utils.is_host_valid(url, hostDict)
				if valid:
					sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,
					                'debridonly': False})
			return sources
		except:
			return sources

	def resolve(self, url):
		return url
