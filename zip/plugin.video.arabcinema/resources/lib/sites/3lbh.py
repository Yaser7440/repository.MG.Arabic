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

import re

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils
progress = utils.progress
Albh_url = 'http://3lbh.net'

@utils.url_dispatcher.register('90')
def TPMain():
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]SEARCH[/B][/COLOR]','https://3lbh.net/search?q=', 94, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]MENU[/B][/COLOR]',Albh_url,99,'','')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]GENRES[/B][/COLOR]',Albh_url + '/movies',95,'','')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]MOVIES[/B][/COLOR]',Albh_url + '/movies',91,'','')	
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]TV SHOWS[/B][/COLOR]',Albh_url + '/eseries',91,'','')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]ARABIC TV SHOWS[/B][/COLOR]',Albh_url + '/aseries',97,'','')
    #utils.addDir('[COLOR red][B]Search[/B][/COLOR]',Albh_url + '/movies?q=',94,'','')
    TPList('http://3lbh.net/movies?page=1',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

#menu
@utils.url_dispatcher.register('99', ['url'])
def menu(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li><a href="([^"]+)">([^"]+)<[^>]+></li>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, menu in match:
        caturl = Albh_url + caturl
        if '/aseries' in caturl:
           utils.addDir('[B]%s[/B]'%utils.cleanspec(menu), caturl, 97, '', '', '')
        else:  
           utils.addDir('[B]%s[/B]'%utils.cleanspec(menu), caturl, 91, '', '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	


def decodeurl(text):
    text = text.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
    return text

#	TV SHOWS & MOVIES
@utils.url_dispatcher.register('91', ['url'], ['page'])
def TPList(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'href="([^"]+)">\s*<[^"]+[^>]+>\s*<img src="([^"]+jpg)[^<]+[^"]+"([^"]+)" />.*?<div class="col-md-6 mIMDB">([^"]+)<[^"]+[^>]+>.+?<p>([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, thumb, name, rating, desc in match:
        thumb = Albh_url + thumb
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        videourl = Albh_url + videourl
        name = name + " [COLOR red]" + rating + "[/COLOR]"
        if '/eseries' in url:
		    utils.addDir('[B]%s[/B]'%utils.cleanspec(name), videourl, 93, thumb, utils.cleantext(desc), '', rating)
        else:		
		    utils.addDownLink('[B]%s[/B]'%utils.cleanspec(name), videourl, 92, thumb, utils.cleantext(desc), '',rating)
    try:
		nextp=re.compile('<li><a href="(.*?)" rel="next">&raquo;</a></li>').findall(listhtml)[0]
		utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]' ,nextp,  91, '')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('97', ['url'], ['page'])
def TPList2(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'href="([^"]+)">\s*<[^"]+[^>]+>\s*<img src="([^"]+jpg)[^<]+[^"]+"([^"]+)" />.*?<p>([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, thumb, name, desc in match:
        thumb = Albh_url + thumb
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        videourl = Albh_url + videourl
        utils.addDir('[B]%s[/B]'%utils.cleanspec(name), videourl, 96, thumb, utils.cleantext(desc), '','')
    try:
		nextp=re.compile('<li><a href="(.*?)" rel="next">&raquo;</a></li>').findall(listhtml)[0]
		utils.addDir('[COLOR red][B]Next Page[/B][/COLOR]' ,nextp,  97, '')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
	
#season
@utils.url_dispatcher.register('93', ['url'])
def SEASON(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<div class="col-md-3+[^>]+">\s*<[^"]+[^>]+>\s*<a href="([^"]+)">\s*<img src="([^"]+jpg)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, thumb, season in match:
        caturl = Albh_url + caturl 
        thumb = Albh_url + thumb 		
        utils.addDir('[B]%s[/B]'%utils.cleanspec(season), caturl, 96, thumb, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)	

#EPISODE
@utils.url_dispatcher.register('96', ['url'])
def episode(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'class="col-md-3+[^"]+[^>]+">\s*<img src="([^"]+)"+[^"]+[^>]+/>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for thumb in match:	
        thumb = Albh_url + thumb
    caturl = utils.getHtml(url, '')
    match = re.compile(r'class="col-md-3+[^"]+[^>]+" href="([^"]+)">\s*<[^>]+>\s*<[^"]+[^>]+><[^>]+>\s*(.+?)\s*</div>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, episode in match:
        caturl = Albh_url + caturl
        if '/aseries' in caturl: 		
            utils.addDownLink('[B]%s[/B]'%utils.cleantext(episode), caturl, 92, thumb, '','')
        else:
            utils.addDownLink('[B]%s[/B]'%utils.cleantext(episode), caturl, 92, thumb, '','')
    xbmcplugin.endOfDirectory(utils.addon_handle)


#GENRES
@utils.url_dispatcher.register('95', ['url'], ['page'])
def GENRES(url, page=1):
    pshtml = utils.getHtml(url, '')
    Regex2 = re.findall(r'<div id="app">(.+?)</div>', pshtml, re.DOTALL)
    for items in Regex2:
      Regex3 = re.findall(r'href="(.+?)">(.+?)</a>', items)
      for url,name in Regex3:
        if 'http' not in url:
           url = Albh_url + url		   
        utils.addDir('[B]%s[/B]'%name, url, 91, '', '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

	
@utils.url_dispatcher.register('92', ['url', 'name'], ['download'])
def TPPlayvid(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    url = url.split('#')[0]
    videopage = utils.getHtml(url, '')
    match1 = re.compile('<title>([^"]+)</title>', re.DOTALL | re.IGNORECASE).findall(videopage)
    for name in match1:
        name = utils.cleantext(name)
    videopage = utils.getHtml(url, '')
    a = re.compile("""<video.*?src=(?:"|')([^"']+)[^>]+>""", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    b = re.compile('''<video.*?src="([^'"]*mp4)''', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    c = re.compile('''"([^'"]*mp4)''', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    videourl = a or b or c
    videourl = videourl.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
    if download == 1:
            utils.downloadVideo(videourl, name)
    else:
            videourl = videourl.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': '[COLOR red][B]MG-Arabic[/B][/COLOR]'})
            xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('98', ['url', 'name'], ['download'])
def TPPlayvid2(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videopage = utils.getHtml(url, '')
    match1 = re.compile('<title>([^"]+)</title>', re.DOTALL | re.IGNORECASE).findall(videopage)
    for name in match1:
        name = utils.cleantext(name)	
    videopage = utils.getHtml(url, '')
    utils.playvideo(videopage, name, download, url)
			

@utils.url_dispatcher.register('94', ['url'], ['keyword'])  
def TPSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 94)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title 
        print "Searching URL: " + searchUrl
        TPList(searchUrl, 1)
