# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.
import re, traceback, urllib
try: from urlparse import urljoin
except ImportError: from urllib.parse import urljoin, unquote
from playscrapers.modules import client, cleantitle, log_utils, source_utils, jsunpack

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['egynow.tv']
        self.base_link = 'https://egynow.tv'
        self.episode_link = '/مشاهدة-مسلسل-%s-موسم-%s-حلقة-%s/'
        self.episode1_link ='/مشاهدة-مسلسل-%s'#-موسم-%s-حلقة-%s/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/?s=%s+%s' % (mtitle, year)
            r = client.request(url)
            results = re.compile('class="BlockItem".+?href="(.+?)"', re.DOTALL).findall(r)
            for url in results:
				url = url
            return url
        except:
            source_utils.scraper_error('EGYNOW')
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			#url = cleantitle.geturl(tvshowtitle)
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = tvshowtitle
			url = url.replace(' ','-')
			# url = self.base_link + '/search/%s/feed/rss2/' % tvshowtitle
			# r = getSum.get(url)
			# items = getSum.findEm(r, '<item>(.+?)</item>')
			# for item in items:
				# match = getSum.findEm(item,'<title>(.+?)</title>.+?<link>(.+?)</link>')
				# for row_title, row_url in match:
					# if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
						# return row_url
			return url
		except:
			source_utils.scraper_error('EGYNOW')
			return
			
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			episode2_link = '/مشاهدة-مسلسل-%s-موسم-%s-حلقة-%s/'
			episode1_link = '/مسلسل-%s-الموسم-%s-الحلقة-%s-مترجمة/'
			episode3_link = '/مشاهدة-مسلسل-%s-الموسم-%s-الحلقة-%s-م/'
			
			r = self.base_link + episode2_link % (tvshowtitle, season , episode)
			r = self.base_link + episode1_link % (tvshowtitle, self.season_fixer(season) , episode)
			r = self.base_link + episode3_link % (tvshowtitle, self.season_fixer(season) , episode)
			url = r
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
            
            links = client.request(url)
            link = re.compile('<li class=" active"(.+?)</table>', re.DOTALL).findall(links)
            for i in link:
				videos = re.compile('src="(.+?)"', re.DOTALL).findall(i)
				for video in videos:
						try:
							video = video.replace('\n','')
							log_utils.log('url = %s' % video, log_utils.LOGDEBUG)
							if any(x in video.lower() for x in ['gounlimited', 'youtube']):
								continue
							if 'vidhd' in video:
								try:
									# loc = re.findall('''https://vidhd.net/embed-(.+?)\r.html''', link, re.DOTALL)[0]
									# link = 'https://vidhd.net/embed-{0}.html'.format(loc)
									data = client.request(video)
									data = re.compile( r'\s*(eval.+?)\s*</script').findall(data)[0]
									link = jsunpack.unpack(data)
									jc = re.compile('file:"(.+?)",label:"(.+?)"', re.DOTALL).findall(link)
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
			log_utils.log('---EGYNOW Testing - Exception: \n' + str(failure))
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