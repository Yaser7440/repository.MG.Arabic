# -*- coding: utf-8 -*-
"""
    ExoScrapers Module

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Addon Name: ExoScrapers Module
# Addon id: script.module.exoscrapers


import os

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

integer = 1000

addon = xbmcaddon.Addon
addonObject = addon('script.module.exoscrapers')
AddonID = addonObject.getAddonInfo('id')
addonInfo = addonObject.getAddonInfo
addonName = addonInfo('name')
addonVersion = addonInfo('version')

lang = addonObject.getLocalizedString
lang2 = xbmc.getLocalizedString

setting = addonObject.getSetting
setSetting = addonObject.setSetting

addItem = xbmcplugin.addDirectoryItem
item = xbmcgui.ListItem
directory = xbmcplugin.endOfDirectory
content = xbmcplugin.setContent
property = xbmcplugin.setProperty

infoLabel = xbmc.getInfoLabel
condVisibility = xbmc.getCondVisibility
jsonrpc = xbmc.executeJSONRPC
window = xbmcgui.Window(10000)
dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()
progressDialogBG = xbmcgui.DialogProgressBG()
windowDialog = xbmcgui.WindowDialog()
button = xbmcgui.ControlButton
image = xbmcgui.ControlImage
getCurrentDialogId = xbmcgui.getCurrentWindowDialogId()
keyboard = xbmc.Keyboard
execute = xbmc.executebuiltin
skin = xbmc.getSkinDir()
player = xbmc.Player()
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
resolve = xbmcplugin.setResolvedUrl
openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir
deleteFile = xbmcvfs.delete
deleteDir = xbmcvfs.rmdir
listDir = xbmcvfs.listdir
transPath = xbmc.translatePath
skinPath = xbmc.translatePath('special://skin/')

# addonPath = xbmc.translatePath(addonInfo('path'))
try:
	addonPath = addonObject.getAddonInfo('path').decode('utf-8')
except:
	addonPath = addonObject.getAddonInfo('path')

SETTINGS_PATH = xbmc.translatePath(os.path.join(addonInfo('path'), 'resources', 'settings.xml'))

# dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
try:
	dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
except:
	dataPath = xbmc.translatePath(addonInfo('profile'))

settingsFile = os.path.join(dataPath, 'settings.xml')
viewsFile = os.path.join(dataPath, 'views.db')
bookmarksFile = os.path.join(dataPath, 'bookmarks.db')
providercacheFile = os.path.join(dataPath, 'providers.13.db')
metacacheFile = os.path.join(dataPath, 'meta.5.db')
searchFile = os.path.join(dataPath, 'search.1.db')
libcacheFile = os.path.join(dataPath, 'library.db')
cacheFile = os.path.join(dataPath, 'cache.db')
key = "RgUkXp2s5v8x/A?D(G+KbPeShVmYq3t6"
iv = "p2s5v8y/B?E(H+Mb"
addonIcon = os.path.join(addonPath, 'icon.png')


def sleep(time):  # Modified `sleep` command that honors a user exit request
	while time > 0 and not xbmc.abortRequested:
		xbmc.sleep(min(100, time))
		time = time - 100


def getKodiVersion():
	return xbmc.getInfoLabel("System.BuildVersion").split(".")[0]


def addonId():
	return addonInfo('id')


def addonName():
	return addonInfo('name')


def version():
	num = ''
	try:
		version = addon('xbmc.addon').getAddonInfo('version')
	except:
		version = '999'
	for i in version:
		if i.isdigit():
			num += i
		else:
			break
	return int(num)


def openSettings(query=None, id=addonInfo('id')):
	try:
		idle()
		execute('Addon.OpenSettings(%s)' % id)
		if query is None:
			raise Exception()
		c, f = query.split('.')
		if int(getKodiVersion()) >= 18:
			execute('SetFocus(%i)' % (int(c) - 100))
			execute('SetFocus(%i)' % (int(f) - 80))
		else:
			execute('SetFocus(%i)' % (int(c) + 100))
			execute('SetFocus(%i)' % (int(f) + 200))
	except:
		return


def getSettingDefault(id):
	import re
	try:
		settings = open(SETTINGS_PATH, 'r')
		value = ' '.join(settings.readlines())
		value.strip('\n')
		settings.close()
		value = re.findall(r'id=\"%s\".*?default=\"(.*?)\"' % (id), value)[0]
		return value
	except:
		return None


def getCurrentViewId():
	win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	return str(win.getFocusId())


def refresh():
	return execute('Container.Refresh')


def busy():
	if int(getKodiVersion()) >= 18:
		return execute('ActivateWindow(busydialognocancel)')
	else:
		return execute('ActivateWindow(busydialog)')


def idle():
	if int(getKodiVersion()) >= 18:
		return execute('Dialog.Close(busydialognocancel)')
	else:
		return execute('Dialog.Close(busydialog)')
