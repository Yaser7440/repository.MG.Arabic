"""
Plugin for UrlResolver
Copyright (C) 2020 gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class faselhdResolver(UrlResolver):
    name = "faselhd"
    domains = ['faselhd.to','tempb06.faseldom.xyz']
    pattern = r'(?://|\.)((?:faselhd|tempb06.faseldom)\.(?:to|xyz))/stream/hls/?(.*?+/v.mp4/index.m3u8)'
	
    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}

        html = self.net.http_GET(web_url, headers=headers).content

        #a = re.compile('''file:"https://tempb06.faseldom.xyz/stream/hls/([^'"])/v.mp4/index.m3u8''').findall(html)[0]
        b = re.compile('''file:"([^'"]+.m3u8)''').findall(html)[0]
        #c = re.compile('''"https://tempb06.faseldom.xyz/stream/hls/(.+?)/v.mp4/index.m3u8''').findall(html)[0]
        stream_url =  b  #[:int(c)] + a[(int(c) + 10):]
        stream_url = base64.b64decode(stream_url)

        return  stream_url + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        return '%s' % media_id
