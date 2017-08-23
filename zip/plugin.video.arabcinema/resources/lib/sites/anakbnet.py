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

anakbnet ='http://www.anakbnet.com'




@utils.url_dispatcher.register('182', ['url'])
def Main(url):
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Search[/B][/COLOR]',anakbnet+'/video/online.php?t=', 183, utils.image('search.png'), '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Categories[/B][/COLOR]',anakbnet+'/video/browse.php?c=2&p=1', 181, '', '')	
    caturl = utils.getHtml(url, '')
    match = re.compile(r'''<li.*?href='([^"]+)' title="([^"]+)"''', re.DOTALL | re.IGNORECASE).findall(caturl)
    for caturl, main in match:
        if caturl.startswith('browse'):
           caturl = 'http://www.anakbnet.com/video/' + caturl
           utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]%s[/B][/COLOR]'%main, caturl, 180, '', '', '')
    try:	
           List(anakbnet+'/video/browse.php?c=2&p=1')           
    except: pass		   
    xbmcplugin.endOfDirectory(utils.addon_handle)




def decodeurl(text):
    text = text.replace(' ','%20').replace('&#039;',"'").replace('&amp;',"&")
    return text
	
@utils.url_dispatcher.register('180', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:        
        return None
    match = re.compile('href="([^"]+)"><img src="([^"]+jpg)".*?title="([^"]+)".*?/></a>.*?<p class="file_description1">([^"]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videourl, thumb, name, desc in match:
        thumb = thumb.replace('&amp;','&').replace(' ','%20').replace('&#039;',"'").replace('\/','/')
        name = utils.cleantext(name)
        utils.addDownLink('[B]%s[/B]'%name, videourl, 188, thumb, 'N/A', desc, 'N/A')
    try:
        nextp=re.compile(r'>>.*?<a href="(.*?)">.*?</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        utils.addDir('Next Page', decodeurl(nextp), 180,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)	
	

@utils.url_dispatcher.register('181', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('''<li.*?href="([^"]+)" title="([^"]+)"''', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        if catpage.startswith('online'):
           catpage = 'http://www.anakbnet.com/video/' + catpage
        utils.addDir('[B]%s[/B]'%name, catpage, 180, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)
	

# @utils.url_dispatcher.register('183', ['url'])
# def Listold(url):
    # try:
        # listhtml = utils.getHtml(url, '')
    # except:        
        # return None
    # match = re.compile(r'<div class="moviefilm">.*?<img.*?src="([^"]+)".*?<div class="movief"><a href="([^"]+)">([^"]+)</a></div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    # for img, videopage, name in match:
        # name = utils.cleantext(name)
        # # if videopage.startswith('/'):
        # #videopage = videopage + '?watch=1'
        # utils.addDownLink(name, videopage, 188, img, '')
    # try:
        # nextp=re.compile(r'<li><a href="([^"]+)">.*? &laquo;</a></li>\s*</ul></div>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        # utils.addDir('Next Page', nextp, 183,'')
    # except: pass
    # xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('183', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 183)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)





# @utils.url_dispatcher.register('173', ['url'])
# def Tags(url):
    # html = utils.getHtml(url, '')
    # match = re.compile('<div class="tagcloud">(.*?)</div>', re.DOTALL | re.IGNORECASE).findall(html)
    # match1 = re.compile("href='([^']+)[^>]+>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(match[0])
    # for catpage, name in match1:
        # utils.addDir(name, catpage, 171, '')
    # xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('188', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
