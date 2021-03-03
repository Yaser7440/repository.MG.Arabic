# -*- coding: utf-8 -*-
"""
    **Created by PressPlay**
    --updated for PressPlay 14/7/2020--
"""

import re, traceback

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus

from playscrapers.modules import log_utils
from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import debrid
from playscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['max-rls.com']
        self.base_link = 'https://max-rls.com'
        self.search_link = '/?s=%s&submit=Find'
        self.headers = {'User-Agent': client.agent()}

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
        try:
            sources = []

            if url is None:
                return sources

            if debrid.status() is False:
                return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)

            query = '%s S%02dE%02d' % (title, int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (title, data['year'])

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('%3A+', '+')

            r = client.request(url)

            posts = client.parseDOM(r, "div", attrs={"class": "postContent"})
            items = []
            for post in posts:
                try:
                    p = client.parseDOM(post, "p", attrs={"dir": "ltr"})[1:]
                    for i in p:
                        items.append(i)
                except:
                    pass

            try:
                for item in items:
                    u = client.parseDOM(item, 'a', ret='href')
                    name = re.findall('<strong>(.*?)</strong>', item, re.DOTALL)[0]
                    name = client.replaceHTMLCodes(name)
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)
                    if not cleantitle.get(t) == cleantitle.get(title): continue
                    for url in u:
                        if any(x in url for x in ['.rar', '.zip', '.iso']): continue
                        quality, info = source_utils.get_release_quality(name, url)
                        try:
                            size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB|gb|mb))', item, re.DOTALL)[0]
                            dsize, isize = source_utils._size(size)
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)
                        info = ' | '.join(info)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                            'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
            except:
                pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---max_rls Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
