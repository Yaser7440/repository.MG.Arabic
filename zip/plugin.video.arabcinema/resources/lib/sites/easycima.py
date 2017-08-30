'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 Fr40m1nd

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
easycima = 'http://www.easycima.com/'

@utils.url_dispatcher.register('400')
def Main():
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Classiques[/B][/COLOR]',easycima + 'dep/dp/1/%D8%A7%D9%81%D9%84%D8%A7%D9%85+%D8%A7%D8%AC%D9%86%D8%A8%D9%89', 401, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Search[/B][/COLOR]','http://www.mrsexe.com/?search=', 404, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Categories[/B][/COLOR]','http://www.mrsexe.com/', 403, '', '')
    utils.addDir('[COLOR red]MG.Arabic[/COLOR] [COLOR white][B]Stars[/B][/COLOR]',easycima + 'dep/dp/1/%D8%A7%D9%81%D9%84%D8%A7%D9%85+%D8%A7%D8%AC%D9%86%D8%A8%D9%89', 405, '', '')
    List(easycima)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('401', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile('class="col-md-3([^<]+)/div>\s</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match1 = re.compile(r'<a rel="([^"]+)" href="([^"]+)">.+? src="([^"]+)".+?/>\n<span class="yeaspro">([^"]+)</span>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name, videopage, img, duration in match1:
        if img.startswith('//'): img = 'http:' + img
        name = utils.cleantext(name) + ' [COLOR red](' + duration + ')[/COLOR]'
        utils.addDir('[B]%s[/B]' %name, videopage, 403, img, '')
    try:
        nextp=re.compile(r'<li class="arrow"><a href="(.+?)">suivant</li>').findall(listhtml)
        utils.addDir('Next Page', 'http://www.mrsexe.com/' + nextp[0], 401,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('404', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 404)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('403', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div class="col-md-3"><a href="([^<]+)" target="_blank"><div class="btn btn-xs btn-success">.*?</div><div class="col-md-3">([^<]+)</div></div>', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 406, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('405', ['url'])
def Stars(url):
    print "mrsexe::Stars " + url
    starhtml = utils.getHtml(url, '')
    match = re.compile(r'<header>\s<h3 class="filles">Les filles de MrSexe</h3>(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(starhtml)
    match1 = re.compile(r'<figure>\s<a href="(.+?)"><img src="(.+?)" alt=""\s/></a>\s</figure>.+?</div>\s<div class="infos">\s<h5><a href=".+?">([^<]+)</a></h5>\s([0-9]+) vid', re.DOTALL | re.IGNORECASE).findall(match[0])
    for starpage, img, name, vidcount in match1:
        name = name + " (" + vidcount + " Videos)"
        utils.addDir(name, 'http://www.mrsexe.com/' + starpage, 401, img)
    try:
        nextp=re.compile(r'<li class="arrow"><a href="(.+?)">suivant</li>').findall(starhtml)
        utils.addDir('Next Page', 'http://www.mrsexe.com/' + nextp[0], 405,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

	
@utils.url_dispatcher.register('406', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    html = utils.getHtml(url, '')
    videourls = re.compile(r'<div class="col-lg-4"><a href="([^<]+)" target="_blank">', re.DOTALL).findall(html)
    for url in videourls:
      utils.PLAYVIDEO(url, name, download)

    xbmcplugin.endOfDirectory(utils.addon_handle)

