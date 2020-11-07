# -*- coding: UTF-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import requests, json, re
import traceback
from exoscrapers.modules import log_utils
from exoscrapers.modules import cleantitle
from exoscrapers.modules import client
from exoscrapers.modules import source_utils
from exoscrapers.modules import control
from exoscrapers.modules import rd_check


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hevcbay.com']
        self.base_link = 'https://hevcbay.com'
        self.movie_link = '/?s=%s+%s'
        self.session = requests.Session()
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % (mtitle.replace('-', '+'), year)
            html = client.request(url, headers=self.headers)
            match = re.compile('<h2 class="entry-title entry--item"><a href="(.+?)" title="(.+?)"').findall(html)
            for url, item_url in match:
                check = '%s (%s)' % (title, year)
                if check not in item_url:
                    continue
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            r = requests.get(url, headers=self.headers).content
            url = re.compile('>Size:</th><td colspan=".+?"> (.+?)<.+?Torrent:</th><td> <a href="(.+?)">Magnet</a>').findall(r)
            for size, url in url:
                url = url.split("&tr=")[0]
                quality, info = source_utils.get_release_quality(url, url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                info.append(size)
                info = ' | '.join(info)
                if control.setting('torrent.rd_check') == 'true':
                    checked = rd_check.rd_cache_check(url)
                    if checked:
                        sources.append(
                            {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                             'info': info, 'direct': False, 'debridonly': True})
                else:
                    sources.append(
                        {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url,
                         'info': info, 'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Hevcbay Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
