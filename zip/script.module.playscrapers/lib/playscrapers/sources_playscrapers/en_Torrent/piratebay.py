# -*- coding: utf-8 -*-

'''
    Playscrapers Project
'''

import simplejson as json
import re, traceback
try:
    from urlparse import parse_qs, urljoin
    from urllib import urlencode, quote, unquote_plus
except ImportError:
    from urllib.parse import parse_qs, urljoin
    from urllib.parse import urlencode, quote, unquote_plus

from playscrapers.modules import cleantitle
from playscrapers.modules import client
from playscrapers.modules import log_utils
from playscrapers.modules import source_utils
from playscrapers.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.base_link = 'https://apibay.org'
        self.search_link = '/q.php?q=%s&cat=0'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('tpb5 - Exception: \n' + str(failure))
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('tpb6 - Exception: \n' + str(failure))
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('tpb7 - Exception: \n' + str(failure))
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        if not url: return sources
        try:
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
            aliases = data['aliases']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s %s' % (title, hdlr)

            url = self.search_link % quote(query)
            url = urljoin(self.base_link, url)

            rjson = client.request(url, error=True)
            #log_utils.log('rjson = ' + str(rjson))
            if not rjson or any(value in rjson for value in ['521 Origin Down', 'No results returned', 'Connection Time-out']):
                return sources
            files = json.loads(rjson)
            for file in files:
                try:
                    _hash = file['info_hash']
                    name = file['name']
                    url = 'magnet:?xt=urn:btih:%s' % (_hash)

                    quality, info = source_utils.get_release_quality(name, url)
                    try:
                        dsize = float(file["size"]) / 1073741824
                        isize = str('%.2f GB' % dsize)
                    except:
                        dsize, isize = 0.0, ''
                    info.insert(0, isize)
                    info = ' | '.join(info)

                    sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                    'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                except:
                    failure = traceback.format_exc()
                    log_utils.log('tpb8 - Exception: \n' + str(failure))
                    continue
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('tpb9 - Exception: \n' + str(failure))
            return sources


    def resolve(self, url):
        return url