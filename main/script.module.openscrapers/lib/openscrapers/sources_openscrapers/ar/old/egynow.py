# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
import traceback
import urllib
from openscrapers.modules import client
from openscrapers.modules import jsunpack
from openscrapers.modules import cleantitle, log_utils
from openscrapers.modules import source_utils
from openscrapers.modules import getSum

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hd.egynow.co']
        self.base_link = 'https://hd.egynow.co'#https://egynow.tv/

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/?s=%s+%s' % (mtitle, year)
            return url
        except:
            source_utils.scraper_error('EGYNOW')
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            r = getSum.get(url)
            results = getSum.findEm(r, 'class="BlockItem".+?href="(.+?)"')
            for url in results:
				links = getSum.get(url)
				link = getSum.findEm(links, '<li class=" active"(.+?)</table>')
				for i in link:
					videos = getSum.findEm(i,'src="(.+?)"')
					for video in videos:
						try:
							video = video.replace('\n','')
							
							if any(x in video.lower() for x in ['gounlimited', 'youtube']):
								continue
							if 'vidhd' in video:
								try:
									# loc = re.findall('''https://vidhd.net/embed-(.+?)\r.html''', link, re.DOTALL)[0]
									# link = 'https://vidhd.net/embed-{0}.html'.format(loc)
									data = getSum.get(video)
									data = getSum.findEm(data, r'\s*(eval.+?)\s*</script')[0]
									link = jsunpack.unpack(data)
									jc = getSum.findEm(link, 'file:"(.+?)",label:"(.+?)"')
									for link, label in jc:
										quality, info = source_utils.get_release_quality(label, label)#[0]
										link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
										sources.append({'source': 'vidhd', 'quality': quality, 'language': 'ar', 'url': link, 'info': info,
														'direct': True, 'debridonly': False})
								except Exception:
									pass													
							elif 'uppom' in video:
								try:
									valid, host = source_utils.is_host_valid(video, hostDict)
									quality, info = source_utils.get_release_quality(video, video)
									video += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), video)
									sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': video,
													'direct': True, 'debridonly': False})
								except Exception:
									pass
							else:	
								valid, host = source_utils.is_host_valid(video, hostDict)
								if valid:
									if host in str(sources):
										continue
									quality, info = source_utils.get_release_quality(video, video)
									sources.append({'source': host, 'quality': quality, 'language': 'ar', 'info': info, 'url': video,
													'direct': False, 'debridonly': False})
						except Exception:
							pass
            return sources
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---WATCHSERIESHD Testing - Exception: \n' + str(failure))
			return sources

    def resolve(self, url):	
            return url