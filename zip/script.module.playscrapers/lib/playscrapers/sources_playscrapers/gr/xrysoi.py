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

import urllib, urlparse, re

from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import source_utils
from playscrapers.modules import dom_parser2
from playscrapers.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['gr']
        self.domains = ['xrysoi.se']
        self.base_link = 'http://xrysoi.se/'
        self.search_link = 'search/%s/feed/rss2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'localtitle': localtitle, 'title': title, 'aliases': aliases,'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            posts = client.parseDOM(r, 'item')

            for post in posts:
                try:
                        name = client.parseDOM(post, 'title')[0]
                        name = client.replaceHTMLCodes(name)

                        t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, re.I)

                        if not re.findall('\w+', cleantitle.get(t))[0] == cleantitle.get(title): raise Exception()

                        y = re.findall('(\d{4}|S\d+E\d+|S\d+)', name, re.I)[0]
                        year = data['year']
                        if not y == year: raise Exception()
                        if not 'tvshowtitle' in data:
                            links = client.parseDOM(post, 'a', ret='href')
                        else:
                            ep = '%02d' % int(data['episode'])
                            pattern = '>Season[\s|\:]%d<(.+?)(?:<b>Season|</content)' % int(data['season'])
                            data = re.findall(pattern, post, re.S|re.I)
                            data = dom_parser2.parse_dom(data, 'a', req='href')
                            links = [(i.attrs['href'], i.content.lower()) for i in data]
                            links = [i[0] for i in links if (hdlr in i[0] or hdlr in i[1] or ep == i[1])]

                        for url in links:
                            if any(x in url for x in ['.online', 'xrysoi.se', 'filmer', '.bp', '.blogger']): continue

                            url = client.replaceHTMLCodes(url)
                            url = url.encode('utf-8')
                            valid, host = source_utils.is_host_valid(url,hostDict)
                            if 'hdvid' in host: valid = True
                            if not valid: continue
                            quality = 'SD'
                            info = 'SUB'

                            sources.append({'source': host, 'quality': quality, 'language': 'gr', 'url': url, 'info': info, 'direct': False, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url