# -*- coding: utf-8 -*-

'''
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

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, unquote_plus, quote_plus
except ImportError: from urllib.parse import urlencode, unquote_plus, quote_plus

from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import debrid
from playscrapers.modules import source_utils
from playscrapers.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yourbittorrent.com', 'yourbittorrent2.com']
        self.base_link = 'https://yourbittorrent.com'
        self.search_link = '/?v=&c=&q=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        self.sources = []
        try:
            if url is None:
                return self.sources

            if debrid.status() is False:
                return self.sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            self.year = data['year']

            query = '%s %s' % (self.title, self.hdlr)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url)
            # log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

            try:
                r = client.request(url)
                links = re.findall('<a href="(/torrent/.+?)"', r, re.DOTALL)

                threads = []
                for link in links:
                    threads.append(workers.Thread(self.get_sources, link))
                [i.start() for i in threads]
                [i.join() for i in threads]
                return self.sources
            except:
                return self.sources

        except:
            return self.sources


    def get_sources(self, link):
        try:
            url = '%s%s' % (self.base_link, link)
            result = client.request(url)

            info_hash = re.findall('<kbd>(.+?)<', result, re.DOTALL)[0]
            url1 = '%s%s' % ('magnet:?xt=urn:btih:', info_hash)
            name = re.findall('<h3 class="card-title">(.+?)<', result, re.DOTALL)[0]
            name = unquote_plus(name).replace(' ', '.')
            url = '%s%s%s' % (url1, '&dn=', str(name))

            t = name.split(self.hdlr)[0].replace(self.year, '').replace('(', '').replace(')', '').replace('&', 'and').replace('.US.', '.').replace('.us.', '.')
            if cleantitle.get(t) != cleantitle.get(self.title):
                return

            if self.hdlr not in name:
                return

            size = re.findall('<div class="col-3">File size:</div><div class="col">(.+?)<', result, re.DOTALL)[0]
            quality, info = source_utils.get_release_quality(name, url)

            try:
                size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', size)[0]
                dsize, isize = source_utils._size(size)
            except:
                dsize, isize = 0.0, ''

            info.insert(0, isize)

            info = ' | '.join(info)

            self.sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})

        except:
            pass

    def resolve(self, url):
        return url
