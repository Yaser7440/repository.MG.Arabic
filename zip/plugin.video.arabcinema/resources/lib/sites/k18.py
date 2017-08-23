'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

import urllib
import re
import sys

import xbmcplugin
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('230')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://watch32.is/',233,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://watch32.is/?s=',234,'','')
    List('http://watch32.is/new-movies/page-1.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('231', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    cookieString = getCookiesString()
    match = re.compile('class="thumb">.*?href="([^"]+)".*?<img src="([^"]+)".*?<a class="title".*?onmouseover="Tip([^"]+), WIDTH,.*?>([^"]+)</a><br>\s+<p>([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, desc, name, genre in match:
        name = utils.cleantext(name)
        name = name.replace('\t','')
        img = img + "|Cookie=" + urllib.quote(cookieString) + "&User-Agent=" + urllib.quote(utils.USER_AGENT)
        utils.addDownLink(name, videopage, 232, img, utils.cleanhtml(desc),genre,'rating')
    try:
        nextp=re.compile('next page-numbers" href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        utils.addDir('Next Page', nextp, 231,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(utils.cookiePath,ignore_discard=True)
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except:
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    return cookieString


@utils.url_dispatcher.register('234', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 234)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('233', ['url'])
def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('0" value="([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        catpage = 'http://k18.co/?cat=' + catpage
        utils.addDir(name, catpage, 231, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)   


@utils.url_dispatcher.register('232', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videopage = utils.getHtml(url, '')
    utils.playvideo(videopage, name, download, url)

