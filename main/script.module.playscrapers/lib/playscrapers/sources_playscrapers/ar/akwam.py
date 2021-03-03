# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, re
import traceback
from playscrapers.modules import client, cleantitle, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['akwam.co']
        self.base_link = 'https://akwam.co'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
		

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/search?q=%s&year=%s' % (mtitle, year)
            r = client.request(url)
            results = re.compile('class="entry-image".+?href="(.+?)"', re.DOTALL).findall(r)
            for url in results:
				url = url
            log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
            return url
        except:
            source_utils.scraper_error('AKWAM')
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:

			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search?q=%s' % mtitle
			
			return url
		except:
			source_utils.scraper_error('AKWAM')
			return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			episode_url = '%01d' % int(episode)
			sea_epi = 'الحلقة-%s' % episode_url
			r = client.request(url, headers=self.headers)
			items = re.compile('class="entry-image">.*?href="(.+?)"\s*class="box">.*?alt="(.+?)"', re.DOTALL).findall(r)
			for url_season, row_season in items:
				if cleantitle.get(self.season_fixer(season)) in cleantitle.get(row_season):
					url_season = url_season
					r = client.request(url_season, headers=self.headers)

					match = re.compile('class="font-size-18 text-white mb-2">.*?href="(.+?)" class="text-white">', re.DOTALL).findall(r)
					for url in match:
						if sea_epi in url:
							return url
							
			return
		except:
			source_utils.scraper_error('AKWAM')
			return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict

            r = client.request(url, headers=self.headers)
            results = re.compile('class="col-lg-3 col".+?href="http://.+?/(.+?)"', re.DOTALL).findall(r)
            for link in results:
				link = link.replace('link','watch')
				if 'episode' in link:
					link = url.replace('episode','%s') % link

				else:
					link = url.replace('movie','%s') % link

				log_utils.log('link = %s' % link, log_utils.LOGDEBUG)	
				d = client.request(link, headers=self.headers)
				videos = re.compile('(?:iframe|source).+?(?:src)=(?:\"|\')(.+?)(?:\"|\')', re.DOTALL).findall(d)
				for video in videos:
						quality = source_utils.check_url(video)
						video = video.replace('https','http')
						#video += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
						sources.append({'source': 'AKWAM', 'quality': quality, 'info': '', 'language': 'ar', 'url': video,
											'direct': True, 'debridonly': False})

            return sources
        except Exception:
			failure = traceback.format_exc()
			log_utils.log('---AKWAM Testing - Exception: \n' + str(failure))
			return sources

    def season_fixer(self, season):
		if '1' in season:
			return 'الأول'
		elif '2' in season:
			return 'الثانى'
		elif '3' in season:
			return 'الثالث'
		elif '4' in season:
			return 'الرابع'
		elif '5' in season:
			return 'الخامس'
		elif '6' in season:
			return 'السادس'
		elif '7' in season:
			return 'السابع'
		elif '8' in season:
			return 'الثامن'
		elif '9' in season:
			return 'التاسع'
		elif '10' in season:
			return 'العاشر'
		elif '11' in season:
			return 'الحادي-عشر'
		elif '12' in season:
			return 'الثاني-عشر'
		elif '13' in season:
			return 'الثالث-عشر'
		elif '14' in season:
			return 'الرابع-عشر'
		elif '15' in season:
			return 'الخامس-عشر'			
		else:
			return 'الأخيرة'

    def resolve(self, url):	
            return url