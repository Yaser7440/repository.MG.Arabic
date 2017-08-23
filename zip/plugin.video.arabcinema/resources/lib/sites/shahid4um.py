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
import xbmc
import re
import xbmcgui
import xbmcplugin
from resources.lib import utils

progress = utils.progress

def decodeurl(text):
    text = text.replace(' ','%20').replace('&#039;',"'").replace('&amp;',"&")
    return text

@utils.url_dispatcher.register('179', ['url'])
def Main(url):
    utils.addDir('[COLOR red][B]Search[/B][/COLOR]','http://shahid4u.com/?s=',174,'','')
    utils.addDir('[COLOR red][B]TV SHOWS[/B][/COLOR]','http://shahid4u.com/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D9%83%D8%AA%D9%85%D9%84%D8%A9',178,'','')
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li id="menu-item-.*?"><a\s*href="([^"]+)">([^"]+)<[^>]+></li>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, menu in match:
        caturl = caturl
  
        utils.addDir('[B]%s[/B]'%menu, caturl, 171, '', '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('171', ['url'], ['page'])
def List(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile('<div class="moviefilm">.*?<img.*?src="([^"]+)".*?<div class="movief"><a href="([^"]+)">([^"]+)<[^>]+><[^>]+>\s*<div class="movieDesc">([^"]+)<[^>]+>\s*</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = utils.cleantext(name)
        # if videopage.startswith('/'):
        videopage = videopage + '?watch=1'
        utils.addDownLink(name, videopage, 170, img, desc, '', 'N/A')
    try:
        nextp=re.compile('<li><a href="(.+?)">.*? &laquo;</a></li>').findall(listhtml)[0]
        utils.addDir('Next Page', nextp, 171,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	
	
	
@utils.url_dispatcher.register('178', ['url'], ['page'])
def TPList(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile('<div class="moviefilm">.*?<img.*?src="([^"]+)".*?<div class="movief"><a href="([^"]+)">([^"]+)<[^>]+><[^>]+>\s*<div class="movieDesc">([^"]+)<[^>]+>\s*</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for thumb, videourl, name, desc in match:
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        utils.addDir('[B]%s[/B]'%name, videourl, 173, thumb, desc, '', 'N/A')
    try:
        nextp=re.compile('href="(.+?)">.*?</a>\s*</div>\s*<[^>]+>\s*<[^>]+>\s*</div>').findall(listhtml)[0]
        utils.addDir('Next Page', nextp, 178,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	
    
@utils.url_dispatcher.register('170', ['url'])	
def resolve(url):
    data = utils.getHtml(url, '')
    if 'rel="shortlink"' in data:
        res_quality = []
        stream_url = []		
        quality = ''						
        regx='rel="shortlink" href=".*?p=(.+?)"'
        id = re.findall(regx,data, re.M|re.I)[0].split("=")[0]
        print "id",id
        for i in range(1,11):
          url='http://shahid4u.com/wp-content/themes/shahid/servers/server.php?q='+id+'&i='+str(i)
          print url
          quality = '[B][COLOR white]SERVER [%s][/COLOR][/B]' %str(i)
          res_quality.append(quality)
          stream_url.append(url)		  
        if len(str(i)) >1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Please Select Servers',res_quality)
            if ret == -1:
                return
            elif ret > -1:
                newurl = stream_url[ret]
        else:
            pass

        SERVER = utils.getHtml(newurl,'')    
        movID = re.compile('src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(SERVER)[0]
        if movID:
            utils.PLAYVIDEO(movID, '', '')
        else:
            utils.notify('Oh oh','Couldn\'t find a video')		
		
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


# @utils.url_dispatcher.register('177', ['url'])
# def Categories(url):
    # cathtml = utils.getHtml(url, '')
    # match = re.compile("Clips</a>(.*)</ul>", re.DOTALL | re.IGNORECASE).findall(cathtml)
    # match1 = re.compile('href="(/[^"]+)[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    # for catpage, name in match1:
        # catpage = 'http://streamxxx.tv' + catpage
        # utils.addDir(name, catpage, 171, '')
    # xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('173', ['url'])
def Tags(url):
    html = utils.Open_Url(url)
    match = re.compile('<div class="movief"><a href="([^<]+)">([^<]+)<[^>]+></div>', re.DOTALL | re.IGNORECASE).findall(html)
    for catpage, name in match:
      catpage = catpage + '?watch=1'	
      utils.addDownLink(name, catpage, 172, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('172', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
