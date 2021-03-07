# -*- coding: utf-8 -*-

'''
	Orion Addon

	THE BEERWARE LICENSE (Revision 42)
	Orion (orionoid.com) wrote this file. As long as you retain this notice you
	can do whatever you want with this stuff. If we meet some day, and you think
	this stuff is worth it, you can buy me a beer in return.
'''

from orion import *
from orion.modules.oriontools import *
from orion.modules.orionnetworker import *

from fenomscrapers.modules import source_utils

try: import urlparse
except: import urllib.parse as urlparse
import urllib
import threading
import pkgutil
import sys
import os
import re
import xbmc
import xbmcaddon

class Orionoid:

	TypeTorrent = OrionStream.TypeTorrent
	TypeHoster = OrionStream.TypeHoster

	TimeDays = 86400
	CacheLimit = 100

	SizeMegaByte = 1048576
	SizeGigaByte = 1073741824

	Keys = {
		'default' : 'VGxOQ1JVbEdSV2ROZVVKVlNVWmpaMU41UVRWSlJXOW5UME5CTlVsRlNXZFZRMEpFU1VWaloxVkRRazlKUmxsblZGTkNUa2xGVldkUlUwSkVTVVUwWjFONVFrVkpSV05uVW5sQ1JFbEVhMmRTVTBKWA==',
		'plugin.video.fen' : 'VTJsQ1EwbEZkMmRPZVVKTlNVVlJaMVpwUVROSlJYZG5VME5DUkVsRlZXZFZVMEpNU1VWeloxRnBRVFJKUlUxblZHbENSMGxGZDJkUlUwSkZTVVZqWjFSRFFUTkpSRkZuVlhsQ1MwbEZSV2RWYVVKSg==',
		'plugin.video.venom' : 'VkdsQ1JVbEZaMmRUYVVFeVNVWlZaMUpwUVROSlJVVm5VV2xDVmtsRk5HZFNRMEV6U1VaaloxSkRRa1ZKUmxsblZHbENVMGxFV1dkU2FVSkVTVVZ2WjFKVFFrZEpSVzluVW5sQ1JVbEZNR2RVYVVKVQ==',
	}

	def __init__(self, type):
		self.type = type
		self.addon = xbmcaddon.Addon('script.module.fenomscrapers')
		profile = xbmc.translatePath(self.addon.getAddonInfo('profile').decode('utf-8'))
		try: os.mkdir(profile)
		except: pass
		self.priority = 1
		self.language = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'nb', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gd', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'is', 'io', 'ig', 'id', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'rn', 'kv', 'kg', 'ko', 'ku', 'kj', 'ky', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lu', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'gv', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'ng', 'ne', 'nd', 'se', 'no', 'ii', 'nn', 'oc', 'oj', 'or', 'om', 'os', 'pi', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'rm', 'ru', 'sm', 'sg', 'sa', 'sc', 'sr', 'sn', 'sd', 'si', 'cu', 'sk', 'sl', 'so', 'nr', 'st', 'es', 'su', 'sw', 'ss', 'sv', 'tl', 'ty', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn', 'tr', 'tk', 'tw', 'uk', 'ur', 'ug', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'za', 'zu']
		self.domains = ['https://orionoid.com']
		self.providers = []
		self.cachePath = os.path.join(profile, 'orion.cache')
		self.cacheData = None
		try: self.key = Orionoid.Keys[xbmcaddon.Addon().getAddonInfo('id')]
		except: self.key = Orionoid.Keys['default']

	def movie(self, imdb, title, aliases, year):
		try: return urllib.urlencode({'imdb' : imdb, 'title' : title, 'year' : year})
		except: return None

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try: return urllib.urlencode({'imdb' : imdb, 'tvdb' : tvdb, 'tvshowtitle' : tvshowtitle, 'year' : year})
		except: return None

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try: return urllib.urlencode({'imdb' : imdb, 'tvdb' : tvdb, 'season' : season, 'episode' : episode})
		except: return None

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return None
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url.update({'title' : title, 'premiered' : premiered, 'season' : season, 'episode' : episode})
			return urllib.urlencode(url)
		except: return None

	def _error(self):
		type, value, traceback = sys.exc_info()
		filename = traceback.tb_frame.f_code.co_filename
		linenumber = traceback.tb_lineno
		name = traceback.tb_frame.f_code.co_name
		errortype = type.__name__
		errormessage = str(errortype) + ' -> ' + str(value.message)
		parameters = [filename, linenumber, name, errormessage]
		parameters = ' | '.join([str(parameter) for parameter in parameters])
		xbmc.log('FENOM SCRAPERS ORION [ERROR]: ' + parameters, xbmc.LOGERROR)

	def _cacheSave(self, data):
		self.cacheData = data
		OrionTools.fileWrite(self.cachePath, OrionTools.jsonTo(data))

	def _cacheLoad(self):
		if self.cacheData == None: self.cacheData = OrionTools.jsonFrom(OrionTools.fileRead(self.cachePath))
		return self.cacheData

	def _cacheFind(self, url):
		cache = self._cacheLoad()
		for i in cache:
			if i['url'] == url:
				return i
		return None

	def _default(self, data):
		return '' if data is None else data

	def _link(self, data):
		links = data['links']
		for link in links:
			if link.lower().startswith('magnet:'):
				return link
		return links[0]

	def _name(self, data):
		return self._default(data['file']['name'])

	def _quality(self, data):
		try:
			quality = data['video']['quality']
			if quality in [Orion.QualityHd8k, Orion.QualityHd6k, Orion.QualityHd4k]:
				return '4K'
			elif quality in [Orion.QualityHd2k]:
				return '1440p'
			elif quality in [Orion.QualityHd1080]:
				return '1080p'
			elif quality in [Orion.QualityHd720]:
				return '720p'
			elif quality in [Orion.QualityScr1080, Orion.QualityScr720, Orion.QualityScr]:
				return 'SCR'
			elif quality in [Orion.QualityCam1080, Orion.QualityCam720, Orion.QualityCam]:
				return 'CAM'
		except: pass
		return 'SD'

	def _language(self, data):
		try:
			language = data['audio']['language']
			if 'en' in language: return 'en'
			return language[0]
		except: return 'en'

	def _source(self, data):
		if data['stream']['type'] == Orion.StreamTorrent:
			return data['stream']['type']
		if data['stream']['type'] == Orion.StreamHoster:
			domain = self._domain(data)
			if domain: return domain
			try:
				if data['stream']['hoster']: return data['stream']['hoster']
			except: pass
			try:
				if data['stream']['source']: return data['stream']['source']
			except: pass
		return None

	def _provider(self, data):
		try: return data['stream']['source']
		except: return None

	def _size(self, data, string = True):
		size = data['file']['size']
		if size:
			if string:
				if size < Orionoid.SizeGigaByte: return '%d MB' % int(size / float(Orionoid.SizeMegaByte))
				else: return '%0.1f GB' % (size / float(Orionoid.SizeGigaByte))
			else:
				return size / float(Orionoid.SizeGigaByte)
		return None

	def _seeds(self, data):
		seeds = data['stream']['seeds']
		if seeds:
			seeds = int(seeds)
			return str(seeds) + ' Seed' + ('' if seeds == 1 else 's')
		return None

	def _days(self, data):
		try: days = (OrionTools.timestamp() - data['time']['updated']) / float(Orionoid.TimeDays)
		except: days = 0
		days = int(days)
		return str(days) + ' Day' + ('' if days == 1 else 's')

	def _popularity(self, data):
		try: popularity = data['popularity']['percent'] * 100
		except: popularity = 0
		return '+' + str(int(popularity)) + '%'

	def _domain(self, data):
		elements = urlparse.urlparse(self._link(data))
		domain = elements.netloc or elements.path
		domain = domain.split('@')[-1].split(':')[0]
		domain = re.sub('(.*?\.).{4,}\..{1,}', '\\1', domain)
		return domain.lower()

	def _debrid(self, data, hosters):
		link = self._link(data)
		if data['stream']['type'] == Orion.StreamTorrent:
			return True
		else:
			for hoster in hosters:
				if hoster in link: return True
		return False

	def sources(self, url, hostDict):
		sources = []
		try:
			if url == None: raise Exception()
			orion = Orion(OrionTools.base64From(OrionTools.base64From(OrionTools.base64From(self.key))).replace(' ', ''))
			if not orion.userEnabled() or not orion.userValid(): raise Exception()

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title'] if 'title' in data else None
			titleEpisode = data['title'] if 'tvshowtitle' in data else None
			year = data['year'] if 'year' in data else None

			imdb = data['imdb'] if 'imdb' in data else None
			tmdb = data['tmdb'] if 'tmdb' in data else None
			tvdb = data['tvdb'] if 'tvdb' in data else None

			season = None
			episode = None
			type = Orion.TypeShow if 'tvshowtitle' in data else Orion.TypeMovie
			if type == Orion.TypeShow:
				try:
					season = int(data['season']) if 'season' in data else None
					episode = int(data['episode']) if 'episode' in data else None
				except: pass
				if season == None or season == '': raise Exception()
				if episode == None or episode == '': raise Exception()
				number = 'S%02dE%02d' % (season, episode)
			else:
				number = year

			results = orion.streams(
				type = type,
				idImdb = imdb,
				idTmdb = tmdb,
				idTvdb = tvdb,
				numberSeason = season,
				numberEpisode = episode,
				streamType = orion.streamTypes(self.type),
				protocolTorrent = Orion.ProtocolMagnet
			)

			for data in results:
				try:
					info = []
					try: info.append(data['stream']['source'])
					except: pass
					try: info.append(data['stream']['hoster'])
					except: pass
					try: info.append(self._seeds(data))
					except: pass
					try: info.append(self._size(data))
					except: pass
					try: info.append('Pack' if data['file']['pack'] else None)
					except: pass
					try: info.append(data['meta']['edition'])
					except: pass
					try: info.append(data['meta']['release'])
					except: pass
					try: info.append(data['meta']['uploader'])
					except: pass
					try: info.append(data['video']['quality'].upper())
					except: pass
					try: info.append(data['video']['codec'].upper())
					except: pass
					try: info.append('3D' if data['video']['3d'] else None)
					except: pass
					try: info.append('%d CH' % data['audio']['channels'] if data['audio']['channels'] else None)
					except: pass
					try: info.append(data['audio']['system'].upper())
					except: pass
					try: info.append(data['audio']['codec'].upper())
					except: pass
					try: info.append('-'.join(data['audio']['languages'].upper()))
					except: pass
					info = [i for i in info if i]

					details = None
					if data['file']['name']:
						details = source_utils.info_from_name(data['file']['name'], title, year, number, titleEpisode)
						if source_utils.remove_lang(details): continue

					orion = {}
					try: orion['stream'] = data['id']
					except: pass
					try: orion['item'] = data
					except: pass

					item = {
						'orion' : orion,
						'provider' : self._provider(data),
						'source' : self._source(data),
						'quality' : self._quality(data),
						'language' : self._language(data),
						'url' : self._link(data),
						'name' : self._name(data),
						'size' : self._size(data, string = False),
						'seeders' : data['stream']['seeds'],
						'info' : ' | '.join(info) if len(info) > 0 else None,
						'name_info' : details,
						'direct' : data['access']['direct'],
						'debridonly' : self._debrid(data, hostDict),
					}
					if data['file']['hash']: item['hash'] = data['file']['hash']

					sources.append(item)
				except: self._error()
		except: self._error()
		self._cacheSave(sources)
		return sources

	def resolve(self, url):
		return url
