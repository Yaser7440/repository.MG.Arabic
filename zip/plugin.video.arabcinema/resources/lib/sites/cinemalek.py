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
import sys

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress
cinemalek = 'https://cinemalek.net/'

@utils.url_dispatcher.register('340')
def Main():
    #utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Search[/B][/COLOR]','https://cinemalek.net/movies/?s=', 343, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]MENU[/B][/COLOR]',cinemalek,346,'','')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Movies[/B][/COLOR]',cinemalek+'category/%D8%A3%D9%81%D9%84%D8%A7%D9%85/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A/', 341, '', '')
    #utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]NEW[/B][/COLOR]',cinemalek, 341, '', '')
    List(cinemalek)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('341', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile(r'class="block_loop">.*?href="([^"]+)" title="([^"]+)">\n.+?<img.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
	if 'movies' not in videopage:
		videopage = videopage.replace('https://cinemalek.net/','https://cinemalek.net/movies/')
        #name = name + " [COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink('[COLOR white][B]%s[/B][/COLOR]' %name, videopage, 342, img, '')
    try:
        nextp=re.compile('<a rel="next" href="(.+?)"  itemprop="name">.*? &rsaquo;</a>').findall(listhtml)
        utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]',nextp[0], 341,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

 
@utils.url_dispatcher.register('343', ['url'], ['keyword']) 
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 343)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('344', ['url'])
def Categories(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(r'<li>\s+<a href="([^"]+)"[^<]+<[^<]+<img.*?src="([^"]+)".*?title">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, img, name in match:
        name = utils.cleantext(name)
        catpage = catpage + '?sortby=post_date'
        utils.addDir(name, catpage, 341, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('345', ['url'])
def Channels(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<A href="([^"]+)"[^<]+<[^<]+<img.*?src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, img, name in match:
        name = utils.cleantext(name)
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 341, img, '')
    # try:
        # nextp=re.compile('href="(/channels/[^"]+)" title="Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        # print "next: ", '' + nextp[0]
        # utils.addDir('Next Page', '' + nextp[0], 345,'')
    # except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('346', ['url'])
def Models(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li id="menu-item-.*?href="([^"]+)" itemprop="name">([^"]+)</a></li>').findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 341, '', '')
    # try:
        # nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        # print "next: ", '' + nextp[0]
        # utils.addDir('Next Page', '' + nextp[0], 346,'')
    # except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('342', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)