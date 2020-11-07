# -*- coding: utf-8 -*-

import sys
try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl

from exoscrapers import sources_exoscrapers
from exoscrapers.modules import control

params = dict(parse_qsl(sys.argv[2].replace('?', '')))
action = params.get('action')
mode = params.get('mode')
query = params.get('query')
name = params.get('name')


if action == "ExoscrapersSettings":
	control.openSettings('0.0', 'script.module.exoscrapers')


elif mode == "ExoscrapersSettings":
	control.openSettings('0.0', 'script.module.exoscrapers')


elif action == 'ShowChangelog':
	from exoscrapers.modules import changelog
	changelog.get()
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == 'ShowHelp':
	from exoscrapers.help import help
	help.get(name)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "Defaults":
	sourceList = []
	sourceList = sources_exoscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		value = control.getSettingDefault(source_setting)
		control.setSetting(source_setting, value)
	# xbmc.log('provider-default = %s-%s' % (source_setting, value), 2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAll":
	sourceList = []
	sourceList = sources_exoscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllPaid":
	sourceList = []
	sourceList = sources_exoscrapers.all_paid_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Paid providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_exoscrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Hoster providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllDebrid":
	sourceList = []
	sourceList = sources_exoscrapers.debrid_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Debrid providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_exoscrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Torrent providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllPackTorrent":
	sourceList = []
	from exoscrapers import pack_sources
	sourceList = pack_sources()
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Pack Torrent providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllForeign":
	sourceList = []
	sourceList = sources_exoscrapers.all_foreign_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Foregin providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")

elif action == "toggleAllArabic":
    sourceList = []
    sourceList = sources_exoscrapers.all_ar_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Arabic providers = %s' % sourceList,2)
    control.sleep(200)
    control.openSettings(query, "script.module.exoscrapers")

elif action == "toggleAllGerman":
	sourceList = []
	sourceList = sources_exoscrapers.german_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All German providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllSpanish":
	sourceList = []
	sourceList = sources_exoscrapers.spanish_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Spanish providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllFrench":
	sourceList = []
	sourceList = sources_exoscrapers.french_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All French providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllGreek":
	sourceList = []
	sourceList = sources_exoscrapers.greek_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Greek providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllKorean":
	sourceList = []
	sourceList = sources_exoscrapers.korean_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Korean providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllPolish":
	sourceList = []
	sourceList = sources_exoscrapers.polish_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Polish providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllRussian":
	sourceList = []
	sourceList = sources_exoscrapers.russian_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])
	# xbmc.log('All Russian providers = %s' % sourceList,2)
	control.sleep(200)
	control.openSettings(query, "script.module.exoscrapers")