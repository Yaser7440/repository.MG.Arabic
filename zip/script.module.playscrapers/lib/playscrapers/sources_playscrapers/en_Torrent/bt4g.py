# -*- coding: utf-8 -*-

'''
    PlayScrapers module

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

import re, traceback

import requests

from six import ensure_text

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, unquote_plus
except ImportError: from urllib.parse import urlencode, unquote_plus

from playscrapers.modules import debrid
from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import source_utils
from playscrapers.modules import log_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bt4g.org']
        self.base_link = 'https://bt4g.org'
        self.search_link = '/movie/search/%s/byseeders/1'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('bt4g0 - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('bt4g1 - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('bt4g2 - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if debrid.status() is False:
                return sources

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))\
                                       if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub(u'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = urljoin(self.base_link, self.search_link % query)
            #log_utils.log('url_is: '+str(url))

            #r = client.request(url)
            r = requests.get(url).content
            r = ensure_text(r).replace('&nbsp;', ' ')
            r = client.parseDOM(r, 'div', attrs={'class': 'col s12'})
            posts = client.parseDOM(r, 'div')[1:]
            posts = [i for i in posts if 'magnet/' in i]
            #log_utils.log('posts_is: '+str(posts))
            for post in posts:

                links = client.parseDOM(post, 'a', ret='href')
                url = ['magnet:?xt=urn:btih:' + i.lstrip('magnet/') for i in links][0]
                try: name = client.parseDOM(post, 'a', ret='title')[0]
                except: name = ''

                quality, info = source_utils.get_release_quality(name, name)
                try:
                    size = re.findall(r'<b class="cpill .+?-pill">(.+?)</b>', post)[0]
                    dsize, isize = source_utils._size(size)
                except:
                    dsize, isize = 0.0, ''

                info.insert(0, isize)

                info = ' | '.join(info)

                sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                'direct': False, 'debridonly': True, 'size': dsize, 'name': name})

            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('bt4g3 - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url