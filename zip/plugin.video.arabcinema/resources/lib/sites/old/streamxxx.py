'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 Fr33m1nd

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


@utils.url_dispatcher.register('170')
def Main():

    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://streamxxx.tv/', 177, '', '')
    #utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/?s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search Scenes[/COLOR]','http://streamxxx.tv/?cat=3673&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/', 175, '', '')
    utils.addDir('[COLOR hotpink]International Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/international-movies/', 176, '', '')
    List('http://streamxxx.tv/category/clips/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('175')
def MainMovies():
    utils.addDir('[COLOR red][B]MENU[/B][/COLOR]','http://shahid4u.com/',179,'','')
    utils.addDir('[COLOR red][B]anakbnet[/B][/COLOR]','http://www.anakbnet.com/video/browse.php?c=2&p=1',180,'','')
    utils.addDir('[COLOR hotpink]MOIVES[/COLOR]','http://shahid4u.com/category/movies/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%89', 171, '', '')
    #utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search Movies[/COLOR]','http://streamxxx.tv/?cat=2212&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]International Movies[/COLOR]','http://streamxxx.tv/category/movies-xxx/international-movies/', 176, '', '')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies-xxx/')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def decodeurl(text):
    text = text.replace(' ','%20').replace('&#039;',"'").replace('&amp;',"&")
    return text
	
@utils.url_dispatcher.register('180', ['url'])
def TPList(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile('href="([^"]+)"><img src="([^"]+jpg)".*?title="([^"]+)".*?/></a>.*?<p class="file_description1">([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, thumb, name, desc in match:
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        utils.addDownLink('[B]%s[/B]'%name, videourl, 172, thumb, 'N/A', desc, 'N/A')
    try:
        nextp=re.compile(r'>>.*?<a href="(.*?)">.*?</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        utils.addDir('Next Page', decodeurl(nextp), 180,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	
#menu
@utils.url_dispatcher.register('179', ['url'])
def menu(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li id="menu-item-.*?"><a\s*href="([^"]+)">([^"]+)<[^>]+></li>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, menu in match:
        caturl = caturl
        if '/aseries' in caturl:
           utils.addDir('[B]%s[/B]'%menu, caturl, 171, '', '', '')
        else:  
           utils.addDir('[B]%s[/B]'%menu, caturl, 171, '', '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	
@utils.url_dispatcher.register('176')
def MainInternationalMovies():
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://streamxxx.tv/', 173, '', '')
    utils.addDir('[COLOR hotpink]Search Overall[/COLOR]','http://streamxxx.tv/?s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Search International Movies[/COLOR]','http://streamxxx.tv/?cat=21&s=', 174, '', '')
    utils.addDir('[COLOR hotpink]Movies[/COLOR]','http://streamxxx.tv/category/movies/', 175, '', '')
    utils.addDir('[COLOR hotpink]Scenes[/COLOR]','http://streamxxx.tv/category/clips/', 170, '', '')
    List('http://streamxxx.tv/category/movies/international-movies/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('171', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'<div class="moviefilm">.*?<img.*?src="([^"]+)".*?<div class="movief"><a href="([^"]+)">([^"]+)</a></div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name in match:
        name = utils.cleantext(name)
        # if videopage.startswith('/'):
        #videopage = videopage + '?watch=1'
        utils.addDownLink(name, videopage, 172, img, '')
    try:
        nextp=re.compile(r'<li><a href="([^"]+)">.*? &laquo;</a></li>\s*</ul></div>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        utils.addDir('Next Page', nextp, 171,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('174', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 174)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('177', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("Clips</a>(.*)</ul>", re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile('href="(/[^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        catpage = 'http://streamxxx.tv' + catpage
        utils.addDir(name, catpage, 171, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('173', ['url'])
def Tags(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="tagcloud">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)
    match1 = re.compile("href='([^']+)[^>]+>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name in match1:
        utils.addDir(name, catpage, 171, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('172', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
