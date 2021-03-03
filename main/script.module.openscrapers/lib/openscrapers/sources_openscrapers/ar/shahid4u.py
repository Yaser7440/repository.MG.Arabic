# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-23-2019 by MGArabic in Scrubs.
# Has shows but is shitty and limited.

import urllib, traceback
from openscrapers.modules import client, log_utils, jsunpack, cleantitle, source_utils, getSum

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['shahid4u.one']
        self.base_link = 'https://shahid4u.one'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.get_url(title).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
            mtitle = cleantitle.geturl(mtitle)
            url = self.base_link + '/search?s=%s+%s' % (mtitle, year)
            r = getSum.get(url, Type='cfscrape')
            results = getSum.findEm(r, 'class="content-box".+?href="(.+?)"')
            for url in results:
				url = url
				return url
			
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---SHAHID4U Testing - Exception: \n' + str(failure))
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			mtitle = cleantitle.get_url(tvshowtitle).replace('-','+').replace(':','').replace('&','+').replace("'",'+')
			mtitle = cleantitle.geturl(mtitle)
			url = self.base_link + '/search?s=%s' % mtitle
			#log_utils.log('SHAHID4U = %s' % url , log_utils.LOGDEBUG)
			r = getSum.get(url)
			items = getSum.findEm(r, 'class="container page-content">(.*?)</div>')
			for item in items:
				match = getSum.findEm(item,'<a href="(.+?)" class="fullClick"></a>')
				for row_url in match:
					if cleantitle.get(tvshowtitle) in cleantitle.get(row_url):
						return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---SHAHID4U Testing - Exception: \n' + str(failure))
			return
			
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			r = getSum.get(url, Type='cfscrape')
			seasons = getSum.findEm(r, 'class="holder-block">(.*?)class="carousel-slider glide">')
			for se in seasons:
				match = getSum.findEm(se,'href="(https://shahid4u.one/season/.+?)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>.+?<span>(.+?)</span></h3></a>')
				for url_season, row_season in match:
					if cleantitle.get(season) in cleantitle.get(row_season):
			 			r = getSum.get(url_season, Type='cfscrape')
						#episodes = getSum.findEm(r, 'class="holder-block">(.*?)class="carousel-slider glide">')
						#for ep in episodes:
						match = getSum.findEm(r,'href="(https://shahid4u.one/episode/.+?)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>.+?<span>(.+?)</span></h3></a>')
						for row_url, row_episode in match:
								if cleantitle.get(episode) in cleantitle.get(row_episode):
									return row_url
			return
		except Exception:
			failure = traceback.format_exc()
			log_utils.log('---SHAHID4U Testing - Exception: \n' + str(failure))
			return



    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostDict + hostprDict
            
            url = url.replace('film','watch').replace('episode','watch')
            r = client.request(url, headers={'User-Agent': client.agent(), 'Referer': url})
            log_utils.log('SHAHID4U = %s' % r , log_utils.LOGDEBUG)
            postid = getSum.findEm(r,'post_id=(.+?)",')
            for postid in postid:
				postid = postid
            serverid = getSum.findEm(r,'data-embedd="(.+?)"')
            for serverid in serverid:
					serverid = serverid
					link = 'https://shahid4u.one/ajaxCenter?_action=getserver&_post_id=%s&serverid=%s' % (postid, serverid)
					log_utils.log('SHAHID4U = %s' % link , log_utils.LOGDEBUG)
					link = link.replace(' ','').replace('https:', '').replace('\r', '')
					link = "https:" + link if not link.startswith('http') else link
					if 'vidhd' in link:
							# loc = re.findall('''https://vidhd.net/embed-(.+?)\r.html''', link, re.DOTALL)[0]
							# link = 'https://vidhd.net/embed-{0}.html'.format(loc)
						
							data = getSum.get(link)
							data = getSum.findEm(data, r'\s*(eval.+?)\s*</script')[0]
							link = jsunpack.unpack(data)
						 	jc = getSum.findEm(link, 'file:"(.+?)",label:"(.+?)"')
						 	for link, label in jc:
								#log_utils.log('url = %s' % link, log_utils.LOGDEBUG)
								quality, info = source_utils.get_release_quality(label, label)#[0]
								link += '|Referer=%s&User-Agent=%s' % (urllib.quote(client.agent()), link)
								#log_utils.log('link = %s' % link, log_utils.LOGDEBUG)
							
								sources.append(
									{'source': 'vidhd', 'quality': quality, 'language': 'ar', 'url': link, 'info': info,
									 'direct': True, 'debridonly': False})
					else:
						valid, host = source_utils.is_host_valid(link, hostDict)
						if not valid: continue
						sources.append(
							{'source': host, 'quality': 'SD', 'language': 'ar', 'url': link, 'info': '',
							 'direct': False, 'debridonly': False})

            return sources
        except:
            source_utils.scraper_error('SHAHID4U')
            return sources

	def resolve(self, url):
		return url