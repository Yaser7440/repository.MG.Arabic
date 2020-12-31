# -*- coding: UTF-8 -*-

# - Converted to py3/2 for PressPlay

import re

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus

from six import ensure_text

from playscrapers.modules import client
from playscrapers.modules import cleantitle
from playscrapers.modules import directstream
from playscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['5movies.to']  # Old  tinklepad.is  movie25.hk
        self.base_link = 'https://5movies.to'
        self.search_link = '/search.php?q=%s'
        self.video_link = '/getlink.php?Action=get&lk=%s'


    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return


    def _search(self, title, year, aliases, headers):
        try:
            q = urljoin(self.base_link, self.search_link % quote_plus(cleantitle.getsearch(title)))
            r = client.request(q)
            r = client.parseDOM(r, 'div', attrs={'class':'ml-img'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'img', ret='alt'))
            url = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and year in i[1]][0][0]
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']
            if 'tvshowtitle' in data:    
                episode = data['episode']
                season = data['season']
                url = self._search(title, year, aliases, headers)
                url = url.replace('online-free', 'season-%s-episode-%s-online-free' % (season, episode))
            else:
                episode = None
                year = data['year']
                url = self._search(data['title'], data['year'], aliases, headers)
            url = url if 'http' in url else urljoin(self.base_link, url)
            result = client.request(url)
            result = client.parseDOM(result, 'li', attrs={'class':'link-button'})
            links = client.parseDOM(result, 'a', ret='href')
            i = 0
            for l in links:
                if i == 20:
                    break
                try:
                    l = l.split('=')[1]
                    l = urljoin(self.base_link, self.video_link % l)
                    result = client.request(l, post={}, headers={'Referer':url})
                    u = result if 'http' in result else 'http:' + result
                    if ' href' in u: u = 'http:' + re.compile(r" href='(.+?)'").findall(u)[0]
                    if 'google' in u:
                        valid, hoster = source_utils.is_host_valid(u, hostDict)
                        urls, host, direct = source_utils.check_directstreams(u, hoster)
                        for x in urls:
                            sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
                    else:
                        valid, hoster = source_utils.is_host_valid(u, hostDict)
                        if not valid:
                            continue
                        try:
                            u = ensure_text(u)
                            sources.append({'source': hoster, 'quality': 'sd', 'language': 'en', 'url': u, 'direct': False, 'debridonly': False})
                            i+=1
                        except:
                            pass
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url


