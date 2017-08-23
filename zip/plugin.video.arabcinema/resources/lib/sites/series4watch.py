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
series4watch_url = 'http://www.series4watch.tv'

@utils.url_dispatcher.register('100')
def TPMain():
    utils.addDir('[COLOR red][B]MENU[/B][/COLOR]',series4watch_url,101,'','')
    utils.addDir('[COLOR red][B]GENRES[/B][/COLOR]',series4watch_url + '/movies',102,'','')
    utils.addDir('[COLOR red][B]MOVIES[/B][/COLOR]',series4watch_url + '/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A/',103,'','')	
    utils.addDir('[COLOR red][B]TV SHOWS[/B][/COLOR]',series4watch_url + '/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A/',103,'','')
    utils.addDir('[COLOR red][B]ARABIC TV SHOWS[/B][/COLOR]',series4watch_url + '/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A/',104,'','')
    #utils.addDir('[COLOR red][B]Search[/B][/COLOR]',series4watch_url + '/movies?q=',108,'','')
    TPList(series4watch_url + '/#',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

#menu
@utils.url_dispatcher.register('101', ['url'])
def menu(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li id="menu-item.*?href="([^"]+)">([^"]+)<[^>]+></li>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, menu in match:
        caturl = caturl
        if '/aseries' in caturl:
           utils.addDir('[B]%s[/B]'%decodename(menu), caturl, 103, '', '', '')
        else:  
           utils.addDir('[B]%s[/B]'%decodename(menu), caturl, 103, '', '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	

def decodename(text):
    text = text.replace('\r','').replace('\n','').replace('\t','')
    return text	
def decodeurl(text):
    text = text.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
    return text

#	TV SHOWS & MOVIES
@utils.url_dispatcher.register('103', ['url'], ['page'])
def TPList(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'<div class="movie">.*?href="([^"]+)">.*?alt="([^"]+)".*?src="([^"]+jpg)".*?<p>([^"]+)</p>.*?<i class="fa fa-star StarLabels"><span>([^"]+)</span></i>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, name, thumb, desc, rating in match:
        thumb = thumb
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        videourl = videourl
        name = name + " [COLOR red]" + rating + "[/COLOR]"
        if '/eseries' in url:
		    utils.addDir('[B]%s[/B]'%decodename(name), videourl + '?view=1', 105, thumb, utils.cleantext(desc), '', rating)
        else:		
		    utils.addDownLink('[B]%s[/B]'%decodename(name), videourl + '?view=1', 106, thumb, utils.cleantext(desc), '',rating)
    try:
		nextp=re.compile('<li><a href="(.*?)">.*?&raquo;</a></li>').findall(listhtml)[0]
		utils.addDir('Next Page ' ,nextp,  103, '')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('104', ['url'], ['page'])
def TPList2(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'href="([^"]+)">\s*<[^"]+[^>]+>\s*<img src="([^"]+jpg)[^<]+[^"]+"([^"]+)" />.*?<p>([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, thumb, name, desc in match:
        thumb = series4watch_url + thumb
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        videourl = series4watch_url + videourl
        utils.addDir('[B]%s[/B]'%decodename(name), videourl, 109, thumb, utils.cleantext(desc), '','')
    try:
		nextp=re.compile('<li><a href="(.*?)" rel="next">&raquo;</a></li>').findall(listhtml)[0]
		utils.addDir('Next Page ' ,nextp,  104, '')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
	
#season
@utils.url_dispatcher.register('105', ['url'])
def SEASON(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<div class="col-md-3+[^>]+">\s*<[^"]+[^>]+>\s*<a href="([^"]+)">\s*<img src="([^"]+jpg)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, thumb, season in match:
        caturl = series4watch_url + caturl 
        thumb = series4watch_url + thumb 		
        utils.addDir('[B]%s[/B]'%decodename(season), caturl, 109, thumb, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)	

#EPISODE
@utils.url_dispatcher.register('109', ['url'])
def episode(url):
    caturl = utils.getHtml(url, '')
    match = re.compile(r'class="col-md-3+[^"]+[^>]+">\s*<img src="([^"]+)"+[^"]+[^>]+/>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for thumb in match:	
        thumb = series4watch_url + thumb
    caturl = utils.getHtml(url, '')
    match = re.compile(r'class="col-md-3+[^"]+[^>]+" href="([^"]+)">\s*<[^>]+>\s*<[^"]+[^>]+><[^>]+>\s*(.+?)\s*</div>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, episode in match:
        caturl = series4watch_url + caturl
        if '/aseries' in caturl: 		
            utils.addDownLink('[B]%s[/B]'%utils.cleantext(episode), caturl, 106, thumb, '','')
        else:
            utils.addDownLink('[B]%s[/B]'%utils.cleantext(episode), caturl, 106, thumb, '','')
    xbmcplugin.endOfDirectory(utils.addon_handle)


#GENRES
@utils.url_dispatcher.register('102', ['url'], ['page'])
def GENRES(url, page=1):
    pshtml = utils.getHtml(url, '')
    Regex2 = re.findall(r'<div id="app">(.+?)</div>', pshtml, re.DOTALL)
    for items in Regex2:
      Regex3 = re.findall(r'href="(.+?)">(.+?)</a>', items)
      for url,name in Regex3:
        if 'http' not in url:
           url = series4watch_url + url		   
        utils.addDir('[B]%s[/B]'%name, url, 103, '', '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

	

@utils.url_dispatcher.register('106', ['url'])
def resolve(url):
    data = utils.getHtml(url, '')
    if 'rel="shortlink"' in data:
        res_quality = []
        stream_url = []		
        quality = ''						
        regx='rel="shortlink" href=".*?p=(.+?)"'
        id = re.findall(regx,data, re.M|re.I)[0].split("=")[0]
        print "id",id
        range=['1','2','3','4','5','6','7','8']
        for i in range:
          url='http://www.series4watch.tv/wp-content/themes/online/servers/server.php?q='+id+'&i='+i
          print url
          quality = '[B][COLOR white]SERVER [%s][/COLOR][/B]' %i
          res_quality.append(quality)
          stream_url.append(url)		  
        if len(range) >1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Please Select Servers',res_quality)
            if ret == -1:
                return
            elif ret > -1:
                newurl = stream_url[ret]
        else:
            pass
        SERVER = utils.getHtml(newurl)    
        movID = re.compile('src="(.*?)"', re.DOTALL | re.IGNORECASE).findall(SERVER)[0]
        if movID:
            utils.addDownLink(quality,110,'','')
        else:
            utils.notify('Oh oh','Couldn\'t find a video')
			
@utils.url_dispatcher.register('110', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videopage = utils.getHtml(url, '')
    utils.playvideo(videopage, name, download, url)
	
@utils.url_dispatcher.register('107', ['url', 'name'], ['download'])
def TPPlayvid2(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile('{source:"([^"]+)", label:', re.DOTALL | re.IGNORECASE).findall(videopage)
    if match:
        videourl = match[0]
        videourl = videourl.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        if download == 1:
            utils.downloadVideo(decodeurl(videourl), name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': '[COLOR red]MG-Arabic[/COLOR]'})
            xbmc.Player().play(videourl, listitem)		    

@utils.url_dispatcher.register('108', ['url'], ['keyword'])  
def TPSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 108)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title 
        print "Searching URL: " + searchUrl
        TPList(searchUrl, 1)
