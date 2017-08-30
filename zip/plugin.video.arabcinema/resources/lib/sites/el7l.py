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
el7l = 'https://el7l.tv/'

@utils.url_dispatcher.register('10')
def Main():
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Search[/B][/COLOR]',el7l+'?s=', 12, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]MENU[/B][/COLOR]',el7l,15,'','')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Categories[/B][/COLOR]',el7l, 13, '', '')	
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Movies[/B][/COLOR]',el7l+'online2/415/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9/1.html', 11, '', '')
    List(el7l)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('11', ['url'], ['page'])
def List(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile(r'class="file_index.*?href="([^"]+)".*?src="([^"]+)".*?<h3>([^"]+)</h3>.*?<p>([^"]+)</p>\n.*?</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img ,name, desc in match:
        name = utils.cleantext(name)
	if 'movies' not in videopage:
		videopage = videopage.replace('/online/','/play/')
        desc = utils.cleanhtml(desc)
        desc = utils.cleantext(desc)
        desc = utils.cleanspec(desc)
        utils.addDownLink('[COLOR white][B]%s[/B][/COLOR]' %name, videopage, 16, img,  desc)
    try:
        nextp=re.compile('<a href="(.*?)">&rsaquo;</a>').findall(listhtml)[0]
        utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]',nextp, 11,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

 
@utils.url_dispatcher.register('12', ['url'], ['keyword']) 
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 12)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('13', ['url'])
def Categories(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(r'<li><a href="([^"]+)".*?>([^"]+)</a></li>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)
        #catpage = catpage + '?sortby=post_date'
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 11, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('14', ['url'])
def Channels(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li><a href="([^"]+)">([^"]+)</a></li>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 341, img, '')
    # try:
        # nextp=re.compile('href="(/channels/[^"]+)" title="Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        # print "next: ", '' + nextp[0]
        # utils.addDir('Next Page', '' + nextp[0], 345,'')
    # except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('15', ['url'])
def Models(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)" title="([^"]+)">.*?</a></li>').findall(listhtml)
    for catpage, name in match:
        name = utils.cleantext(name)
        utils.addDir('[COLOR white][B]%s[/B][/COLOR]' %name, catpage, 11, '', '')
    # try:
        # nextp=re.compile('<a href="(.+?)" title="Next Page" data-page-num.+?>Next page').findall(listhtml)
        # print "next: ", '' + nextp[0]
        # utils.addDir('Next Page', '' + nextp[0], 346,'')
    # except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('16', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)