'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream

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
import xbmcgui
import xbmcplugin
from resources.lib import utils
cimaclub = 'http://cimaclub.com/' 
progress = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
@utils.url_dispatcher.register('450', ['url'])
def Main(url):
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]GENRES[/B][/COLOR]',cimaclub,453,'','')
    caturl = utils.getHtml(url, '')
    match = re.compile(r'<li id="menu-item-.*?href="([^"]+)">([^"]+)</a></li>', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, menu in match:
        utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]%s[/B][/COLOR]'%menu, caturl, 451, '', '', '')
    List(cimaclub)
    xbmcplugin.endOfDirectory(utils.addon_handle)




	
@utils.url_dispatcher.register('451', ['url'], ['page'])
def List(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile(r'class="movie">.*?href="([^"]+)".*?<img alt="([^"]+)" src="([^"]+)".*?<p>([^"]+)</p>.*?<i class="fa fa-star StarLabels"><span>([^"]+)</span></i>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, name, thumb, desc, rating in match:
        thumb = thumb
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        desc = desc.replace('\r','').replace('\n','').replace('\t','')
        name = name + " [COLOR red]" + rating + "[/COLOR]"
        if '/cat/' in url:
		    utils.addDir('[B]%s[/B]'%name, videourl , 452, thumb, '', '', '')
        else:		
		    utils.addDownLink('[B]%s[/B]'%name, videourl, 452, thumb, desc, '','')
    try:
		nextp=re.compile('<li><a href="([^"]+)">.*?&laquo;</a></li>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
		utils.addDir('Next Page ' ,nextp,  451, '')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)



@utils.url_dispatcher.register('452', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    data = utils.getHtml(url, '')
    if 'p=' in data:
        res_quality = []
        stream_url = []		
        quality = ''						
        regx='\?p=([^"]+)"'
        id = re.findall(regx,data, re.M|re.I)[0].split("=")[0]
        print "id",id
        range=['1','2','3','4','5','6','7','8']
        for i in range:
          url='http://cimaclub.com/wp-content/themes/Cimaclub/servers/server.php?q='+id+'&i='+i
          print url
          quality = '[B][COLOR white]SERVER [%s][/COLOR][/B]' %i
          res_quality.append(quality)
          stream_url.append(url)		  
        if len(range) >1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Please Select Servers',res_quality)
            if ret == 0:		
                return
            elif ret > 1:
                newurl = res_quality[ret]
        else:
            pass
        SERVER = utils.getHtml(newurl, url)    
        videourl = re.compile('src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(SERVER)[0]
        if videourl:
            utils.PLAYVIDEO(videourl, name, download)
        else:
            utils.notify('Oh oh','Couldn\'t find a video')
			
@utils.url_dispatcher.register('453', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="(http://cimaclub.com/genre/[^"]+)">.*?<span>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 451, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('454', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 454)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)
		
@utils.url_dispatcher.register('455', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
