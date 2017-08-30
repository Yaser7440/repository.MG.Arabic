'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 anton40

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
'''

import re

import xbmcplugin
from resources.lib import utils

progress = utils.progress
cimamix = 'https://cimamix.net/'


@utils.url_dispatcher.register('245')
def MainMovies():
    #utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]SEARCH[/B][/COLOR]',cimamix + '?s=', 244, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]MENU[/B][/COLOR]',cimamix,246,'','')	
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Categories[/B][/COLOR]',cimamix,247,'','')	
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Movies[/B][/COLOR]',cimamix + 'c/10/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9/1.html', 241, '', '')
    List(cimamix)
    xbmcplugin.endOfDirectory(utils.addon_handle)

	
@utils.url_dispatcher.register('246', ['url'])
def MENU(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li id=.*?<a href="([^"]+)">([^"]+)</a></li>').findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 241, '', '')
    # try:
        # nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        # print "next: ", '' + nextp[0]
        # utils.addDir('Next Page', '' + nextp[0], 346,'')
    # except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
@utils.url_dispatcher.register('247', ['url'])
def Categories(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li><a href="([^"]+)">([^<]+)</a></li>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)       
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 243, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)
	
@utils.url_dispatcher.register('241', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile('href="([^"]+)">\s*<img src="([^"]+)".*?alt="([^"]+)"').findall(listhtml)
    for videopage, img, name in match:
        print "Processing: " + name
        name = utils.cleantext(name)
        videopage = videopage.replace("/f/","/play/")
        utils.addDownLink('[COLOR white][B]%s[/B][/COLOR]' %name, videopage, 242, img, '')
    try:
        print "Adding next"
        nextp=re.compile('</a>...<a href="(.+?)">&.*?</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        if 'cimamix' not in nextp:
         nextp = cimamix + nextp
        utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]', nextp, 241,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('243', ['url'])
def ListCategories(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile('href="([^"]+)">\s*<img src="([^"]+)".*?alt="([^"]+)"').findall(listhtml)
    for videopage, img, name in match:
        print "Processing: " + name
        name = utils.cleantext(name)
        videopage = videopage.replace("/f/","/play/")
        utils.addDownLink('[COLOR white][B]%s[/B][/COLOR]' %name, videopage, 242, img, '')
    try:
        print "Adding next"
        nextp=re.compile('<a href="(.+?)" class="next">', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        if 'cimamix' not in nextp:
         nextp = cimamix + nextp
        utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]', nextp, 243,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
	
@utils.url_dispatcher.register('244', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 244)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('242', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
