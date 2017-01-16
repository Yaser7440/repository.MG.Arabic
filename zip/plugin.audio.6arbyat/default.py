# -*- coding: utf-8 -*-Edit By-MG.Arabic





try:import sys, syspath
except:pass
import os, sys
import httplib
import time
from urllib import urlencode
import urllib, urllib2, re, sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse


import StringIO

__settings__ = xbmcaddon.Addon(id='plugin.audio.6arbyat')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = sys.argv[0]
baseurl = 'http://www.6arbyat.com/'

####functions

def read_url(url):
     
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', host)
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
        return link
    
def readnet2(url):
            from addon.common.net import Net
            net=Net()
            USER_AGENT='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0'
            MAX_TRIES=3
            


            
            headers = {
                'User-Agent': USER_AGENT,
                'Referer': url
            }

            html = net.http_GET(url).content
            return html
      

              
def gethostname(url):
        from urlparse import parse_qs, urlparse
        query = urlparse(url)
        
        return query.hostname 
##########################################parsing tools
def showmenu():

                genreliste=[('cat/saudi-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb3\xd8\xb9\xd9\x88\xd8\xaf\xd9\x8a\xd8\xa9'),
				('cat/kuwaiti-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x83\xd9\x88\xd9\x8a\xd8\xaa\xd9\x8a\xd8\xa9'),
				('cat/bahraini-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xa8\xd8\xad\xd8\xb1\xd9\x8a\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/uae-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xa7\xd9\x85\xd8\xa7\xd8\xb1\xd8\xa7\xd8\xaa\xd9\x8a\xd8\xa9'),
				('cat/qatar-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x82\xd8\xb7\xd8\xb1\xd9\x8a\xd8\xa9'),
				('cat/omani-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb9\xd9\x85\xd8\xa7\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/yemeni-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x8a\xd9\x85\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/iraqi-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb9\xd8\xb1\xd8\xa7\xd9\x82\xd9\x8a\xd8\xa9'),
				('cat/lebanese-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x84\xd8\xa8\xd9\x86\xd8\xa7\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/jordan-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xa7\xd8\xb1\xd8\xaf\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/palestinian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x81\xd9\x84\xd8\xb3\xd8\xb7\xd9\x8a\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/syrian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb3\xd9\x88\xd8\xb1\xd9\x8a\xd8\xa9'),
				('cat/egyptian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x85\xd8\xb5\xd8\xb1\xd9\x8a\xd8\xa9'),
				('cat/sudanese-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb3\xd9\x88\xd8\xaf\xd8\xa7\xd9\x86\xd9\x8a\xd8\xa9'),
				('cat/moroccan-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x85\xd8\xba\xd8\xb1\xd8\xa8\xd9\x8a\xd8\xa9'),
				('cat/tunisian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xaa\xd9\x88\xd9\x86\xd8\xb3\xd9\x8a\xd8\xa9'),
				('cat/algerian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xac\xd8\xb2\xd8\xa7\xd8\xa6\xd8\xb1\xd9\x8a\xd8\xa9 '),
				('cat/libyan-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd9\x84\xd9\x8a\xd8\xa8\xd9\x8a\xd8\xa9 '),
				('cat/arabian-songs/', '\xd8\xa7\xd8\xba\xd8\xa7\xd9\x86\xd9\x8a \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd8\xa9'),
				('cat/concerts/', '\xd8\xad\xd9\x81\xd9\x84\xd8\xa7\xd8\xaa \xd9\x88 \xd8\xac\xd9\x84\xd8\xb3\xd8\xa7\xd8\xaa '),
				('hashtag/\xd8\xba\xd9\x8a\xd8\xb1_\xd9\x85\xd8\xad\xd8\xaf\xd8\xaf/', '\xd8\xba\xd9\x8a\xd8\xb1_\xd9\x85\xd8\xad\xd8\xaf\xd8\xaf'),
				('hashtag/\xd9\x85\xd9\x87\xd8\xb1\xd8\xac\xd8\xa7\xd9\x86\xd8\xa7\xd8\xaa/', '\xd9\x85\xd9\x87\xd8\xb1\xd8\xac\xd8\xa7\xd9\x86\xd8\xa7\xd8\xaa'),
				('hashtag/\xd8\xb4\xd9\x8a\xd9\x84\xd8\xa9/', '\xd8\xb4\xd9\x8a\xd9\x84\xd8\xa9'),
				('hashtag/\xd8\xb3\xd9\x86\xd9\x82\xd9\x84/', '\xd8\xb3\xd9\x86\xd9\x82\xd9\x84'),
				('hashtag/\xd8\xb3\xd8\xa7\xd9\x85\xd8\xb1\xd9\x8a\xd8\xa7\xd8\xaa/', '\xd8\xb3\xd8\xa7\xd9\x85\xd8\xb1\xd9\x8a\xd8\xa7\xd8\xaa'), ('hashtag/\xd8\xb4\xd8\xb9\xd8\xa8\xd9\x8a\xd8\xa7\xd8\xaa/', '\xd8\xb4\xd8\xb9\xd8\xa8\xd9\x8a\xd8\xa7\xd8\xaa'),
				('hashtag/\xd8\xb1\xd9\x8a\xd9\x85\xd9\x83\xd8\xb3\xd8\xa7\xd8\xaa/', '\xd8\xb1\xd9\x8a\xd9\x85\xd9\x83\xd8\xb3\xd8\xa7\xd8\xaa'), ('hashtag/\xd8\xad\xd9\x81\xd9\x84\xd8\xa7\xd8\xaa/', '\xd8\xad\xd9\x81\xd9\x84\xd8\xa7\xd8\xaa'),
				('hashtag/\xd9\x85\xd8\xb3\xd9\x84\xd8\xb3\xd9\x84\xd8\xa7\xd8\xaa/', '\xd9\x85\xd8\xb3\xd9\x84\xd8\xb3\xd9\x84\xd8\xa7\xd8\xaa'), ('hashtag/\xd9\x88\xd8\xb7\xd9\x86\xd9\x8a\xd8\xa7\xd8\xaa/', '\xd9\x88\xd8\xb7\xd9\x86\xd9\x8a\xd8\xa7\xd8\xaa'),
				('hashtag/\xd9\x85\xd9\x88\xd8\xb4\xd8\xad\xd8\xa7\xd8\xaa/', '\xd9\x85\xd9\x88\xd8\xb4\xd8\xad\xd8\xa7\xd8\xaa'),
				('hashtag/\xd9\x85\xd9\x88\xd8\xa7\xd9\x88\xd9\x8a\xd9\x84/', '\xd9\x85\xd9\x88\xd8\xa7\xd9\x88\xd9\x8a\xd9\x84'),
				('hashtag/\xd8\xac\xd9\x84\xd8\xb3\xd8\xa7\xd8\xaa/', '\xd8\xac\xd9\x84\xd8\xb3\xd8\xa7\xd8\xaa'),
				('hashtag/\xd9\x82\xd8\xb5\xd8\xa7\xd8\xa6\xd8\xaf/', '\xd9\x82\xd8\xb5\xd8\xa7\xd8\xa6\xd8\xaf')]
                            
                addDir("احدث الأعمال الفنية", 'http://www.6arbyat.com/aghany-songs/?page=1',1001,'resources/6.png','',1)                
		#addDir("جديد الألبومات", 'http://www.6arbyat.com/',100,'resources/6.png','',1)
                
                #addDir("Search", 'http://www.6arbyat.com/search?q=',3,'resources/search.png','',1)
                for url, title  in genreliste:
                    url='http://www.6arbyat.com/'+url
                    if 'اغاني' in title:
                      addDir(title, url, 100, '','',1)
                    else:
                       addDir(title, url,1001, '','',1)     

def search(url):
        
        
         
        search_entered = ''
        debug=True
        if debug:
               keyboard = xbmc.Keyboard(search_entered, 'Search 1channel')
               keyboard.doModal()
               if keyboard.isConfirmed():
                   search_entered = keyboard.getText() .replace(' ','+')  
                   
                   
        else:
             print "search error"
            
        
        
         
        url= url+search_entered

        getartists("Search",url,1)
                                           

def getartists(tname,urlmain,page):##series
                if page>1:
                  #/page/2/http://tvgate.tv/english-movies/2/
                  #     
                  url_page=urlmain+str(page-1)+"/"
                  
                else:
                
                      url_page=urlmain
                data=readnet2(url_page)
                try:data=data.split('<div class="row contentofcats">')[1]
                except:pass
                
               
                if data is None:
                    return
                #print dataclass="vi-box-top"
                blocks=data.split('<li class="col-md-4 col-sm-4">')
                i=0
                
               
                for block in blocks:
                    i=i+1
                    if i==1:
                            continue
                    
                   
                    
                    regx="<a href='(.*?)'>"
                    
                    try:href=re.findall(regx,block, re.M|re.I)[0]
                    except:continue
                    href='http://www.6arbyat.com/'+href
                    
                    
                    regx='''<img alt='(.*?)' src='(.*?)'/>'''
                    match=re.findall(regx,block, re.M|re.I)
                    img='http://www.6arbyat.com/'+match[0][1]
                    name=match[0][0]
                   
                    
                    
                    
                   
                                             
                               
                    
                    try:name=name.encode("utf-8")
                    except:name=str(name)
                    
                    try:addDir(name,href,1000,img,'',1)
                    except:continue
               
                if len(blocks)>7:
                   addDir("next page",urlmain,100,'special://home/addons/plugin.audio.6arbyat/resources/nextpage.jpg','',str(page+1))                
                if len(blocks)==0:
                    addDir("Error:no results",urlmain,100,'','',str(page+1))

					
def getsongs(tname,urlmain,page):##series
                if page>1:
                  #/page/2/http://tvgate.tv/english-movies/2/
                  #     
                  url_page=urlmain+str(page-1)+"/"
                  
                else:
                
                      url_page=urlmain
                data=readnet2(url_page)
                try:data=data.split('<div class="conti">')[1]
                except:pass
                
               
                if data is None:
                    return
                #print dataclass="vi-box-top"
                blocks=data.split("<div class='col-md-2'>")
                i=0
                
               
                for block in blocks:
                    i=i+1
                    if i==1:
                            continue
                    
                   
                    
                    regx="<a href='(.*?)'"
                    
                    try:href=re.findall(regx,block, re.M|re.I)[0]
                    except:continue
                    href='http://www.6arbyat.com/'+href
                    
                    
                    regx='''<img alt='(.*?)' src='(.*?)'/>'''
                    match=re.findall(regx,block, re.M|re.I)
                    img='http://www.6arbyat.com/'+match[0][1]
                    name=match[0][0]
                   
                    
                    
                    
                   
                                             
                               
                    
                    try:name=name.encode("utf-8")
                    except:name=str(name)
                    
                    try:addDir(name,href,1001,img,'',1)
                    except:continue
                    
               
                # if len(blocks)>7:
                   # addDir("next page",urlmain,1000,'special://home/addons/plugin.audio.6arbyat/resources/nextpage.jpg','',str(page+1))                
                # if len(blocks)==0:
                    # addDir("Error:no results",urlmain,1000,'','',str(page+1))

def getsongs2(tname,urlmain,page):##series
                if page>1:
                  #/page/2/http://tvgate.tv/english-movies/2/
                  #     
                  url_page=urlmain+str(page-1)+"/"
                  
                else:
                
                      url_page=urlmain
                data=readnet2(url_page)
                try:data=data.split('<div class="col-md-5 songsofalbum">')[1]
                except:pass
                
               
                if data is None:
                    return
                #print dataclass="vi-box-top"
                blocks=data.split("<ul>")
                i=0
                
               
                for block in blocks:
                    i=i+1
                    if i==1:
                            continue
                    
                   
                    
                    regx='''<a href='(.*?)'>(.*?)</a>'''
                    
                    match=re.findall(regx,block, re.M|re.I)
                    print "block",block.encode("utf-8")
                    print "match",match
                    try:href='http://www.6arbyat.com'+match[0][0]
                    except:continue
                    
                    name=match[0][1]              
                               
                    
                    try:name=name.encode("utf-8")
                    except:name=str(name)
                    
                    addDir(name,href,1,'','',1)
                    
               
                # if len(blocks)>7:
                   # addDir("next page",urlmain,1001,'special://home/addons/plugin.audio.6arbyat/resources/nextpage.jpg','',str(page+1))                
                # if len(blocks)==0:
                    # addDir("Error:no results",urlmain,1001,'','',str(page+1))                    


#######################################host resolving                                                    
# def creatertmp(host,urlmain):
     # #rtmp://streaming.hayyes.com/vod/<playpath>mp4:29/29303/29303_1_400k.mp4 <swfUrl>http://www.hayyes.com/sites/all/themes/hys/tpl/jw/jwplayer.flash.swf <pageUrl>http://www.hayyes.com/vod/aflam/7alawet-roo7
     # url=host+'  swfUrl=http://www.hayyes.com/sites/all/themes/hys/tpl/jw/jwplayer.flash.swf pageUrl='+ urlmain
     # return url

def gethosts(name,urlmain):##cinema and tv featured
#href="http://www.arabshow.tv/the-forest/2/">
        data=readnet2(urlmain)
        regx='<meta property="og:audio" content="(.*?)"/>'
        regx='<meta property="og:audio" content="(.*?)"/>'
        
        
        link=re.findall(regx,data, re.M|re.I)[0]
        playlink(link)
       
        
       

def playlink(url):
            print "m2",url
            xbmc.Player().play(url)
            sys.exit(0)
	    listItem = xbmcgui.ListItem(path=str(url))
	    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

            
############################################xbmc tools	    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        print "input,output",paramstring,param
        return param



def addLink(name,url,mode,iconimage):
        
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok
	
def addDir(name,url,mode,iconimage,extra='',page=0):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def getgroups(data, pattern, grupsNum = 1, ignoreCase = False):
        tab = []
        if ignoreCase:
            match = re.search(pattern, data, re.IGNORECASE)
        else:
            match = re.search(pattern, data)
        
        for idx in range(grupsNum):
            try:
                value = match.group(idx + 1)
            except:
                value = ''

            tab.append(value)

        return tab
def getdata(data, marker1, marker2, withMarkers = True, caseSensitive = True):
        if caseSensitive:
            idx1 = data.find(marker1)
        else:
            idx1 = data.lower().find(marker1.lower())
        if -1 == idx1:
            return (False, '')
        if caseSensitive:
            idx2 = data.find(marker2, idx1 + len(marker1))
        else:
            idx2 = data.lower().find(marker2.lower(), idx1 + len(marker1))
        if -1 == idx2:
            return (False, '')
        if withMarkers:
            idx2 = idx2 + len(marker2)
        else:
            idx1 = idx1 + len(marker1)
        return  data[idx1:idx2]

params=get_params()
url=None
name=None
mode=None
page=1

	
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "page: "+str(page)

if mode==None or url==None or len(url)<1:
        print ""
        showmenu()
elif mode==1:
        print ""+url
        gethosts(name,url)
       

elif mode==2:
        print ""+url
        playlink(url)
elif mode==3:
        search(url)        
        
elif mode==100:
        print ""+url
        getartists(name,url,page)

elif mode==1000:
        print ""+url
        getsongs(name,url,page)        
elif mode==1001:
         print ""+url
         getsongs2(name,url,page)     




xbmcplugin.endOfDirectory(int(sys.argv[1]))                                 
