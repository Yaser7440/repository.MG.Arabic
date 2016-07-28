# -*- coding: utf8 -*-
try:import sys, syspath
except:pass
import sys
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib
import time,itertools

__settings__ = xbmcaddon.Addon(id='plugin.video.aflamy')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])
baseurl='http://www.aflamy.com/'


def read_url(url):
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

def getCategories():
	addDir('search','http://www.aflamy.com/',13,'special://home/addons/plugin.video.aflamy/img/SEARCH.png',1)
        addDir('••أخــر الاضافات••','http://www.aflamy.com/online/',11,'special://home/addons/plugin.video.aflamy/img/LAST.png',1)
	addDir('أفـــلام اجنبية','http://www.aflamy.org/category/aflam-ajnaby/',11,'special://home/addons/plugin.video.aflamy/img/mov.png',1)
        addDir('أفــلام عربية','http://www.aflamy.com/online/category/aflam-araby/',11,'special://home/addons/plugin.video.aflamy/img/AR.png',1)                      
        addDir('أفــلام هندية','http://www.aflamy.com/online/category/aflam-hindy/',11,'special://home/addons/plugin.video.aflamy/img/BOL.png',1)  
        addDir('افلام ممنوعه من العرض','http://www.aflamy.pw/portal/category/aflam-llekbar/',11,'special://home/addons/plugin.video.aflamy/img/',1)                                       
        addDir('أفــلام الانيمي','http://www.aflamy.pw/portal/category/aflam-animy/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('مسرحيات','http://www.aflamy.pw/portal/category/msr7yat/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        addDir('مسلسلات عربي','http://www.aflamy.pw/portal/category/moslslat-araby/',11,'special://home/addons/plugin.video.aflamy/img/AR.png',1)
        addDir('مسلسلات تركي','http://www.aflamy.pw/portal/category/moslslat-turkey/',11,'special://home/addons/plugin.video.aflamy/img/5.png',1)
        addDir('مسلسلات اجنبي','http://www.aflamy.pw/portal/category/moslslat-ajnaby/',11,'special://home/addons/plugin.video.aflamy/img/YEARS.png',1)
        #addDir('مسلسلات اسيويه','http://www.aflamy.pw/portal/category/asian-seriess/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        addDir('مصارعه','http://www.aflamy.pw/portal/category/wwe-mosr3a/',11,'special://home/addons/plugin.video.aflamy/img/WWE.png',1)
        #addDir('كوره','http://www.aflamy.pw/portal/category/football-koora/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('اخبار','http://www.aflamy.pw/portal/category/akhbar-news/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('العاب','http://www.aflamy.pw/portal/category/games-al3ab/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('اغاني','http://www.aflamy.pw/portal/category/clips-mp3-aghany/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('برامج كامله','http://www.aflamy.pw/portal/category/bramj-full/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        addDir('توك شو','http://www.aflamy.pw/portal/category/talk-show-online/',11,'special://home/addons/plugin.video.aflamy/img/',1)
        #addDir('مسلسلات هنديه','http://www.aflamy.pw/portal/category/hindi-series/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('مسلسلات مكسيكيه','http://www.aflamy.pw/portal/category/mexican-series/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        addDir('افلام اسيويه','http://www.aflamy.pw/portal/category/asian-movies/',11,'special://home/addons/plugin.video.aflamy/img/',1)
       # addDir('ابراج','http://www.aflamy.pw/portal/category/abraj/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
       # addDir(' 2014رمضان','http://www.aflamy.pw/portal/category/ramadan-series-2014/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('مسلسلات اسيوه','http://www.aflamy.pw/portal/category/asian-series-arabic/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1)
        #addDir('فلاش انلين','http://www.aflamy.pw/portal/category/online-flash-games/',11,'special://home/addons/plugin.video.aflamy/img/CARTOON.png',1) 
        

        
      
def search(url):
         
        search_entered = ''
        debug=True
        if debug:
               keyboard = xbmc.Keyboard(search_entered, 'Search 1channel')
               keyboard.doModal()
               if keyboard.isConfirmed():
                   search_entered = keyboard.getText() .replace(' ','+')  
                   print "mfarajx3",search_entered
                   
        else:
             print "search error"
            
        
        
         
        url="http://www.aflamy.com/online/?s="+search_entered
        print "mfarajx4_url",url
          
        getVideos("Search",url,1)
        
        
def getVideos(name1, urlmain,page):
               print "mahmou1",urlmain
               print "page",page
               
               if page>1 :
                  
                  url_page=urlmain+'/page/'+str(page)
                  
               else:
                #http://www.dardarkom.com/filme-enline/filme-gharbi/page/2/
                      url_page=urlmain
               print "url_page",url_page
               
               data = read_url(url_page)                 
               
             
               if data is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               blocks=data.split('<h1 class="post-title">')
               i=0
                
               
               for block in blocks:
                    i=i+1
                    if i==1:
                            continue
                   
                    
                    regx='''<a href="(.*?)">(.*?)</a>'''
                    
                    match=re.findall(regx,block, re.M|re.I)
                    name=match[0][1]
                    href=match[0][0]
                    regx="<img src='(.*?)'"
                    img=re.findall(regx,block, re.M|re.I)[0]
                    
                    
                    

                    
                    
                                                
                               
                    
                    try:name=name.encode("utf-8")
                    except:name=str(name)
                    try:addDir(name,href,2,img,1)
                    except:pass
               
                   
                
                
               addDir("next page",urlmain,100,'http://www.tachyonpunch.com/comics/images/next_icon.png',str(page+1))
               if len(blocks)==0:
                    addDir("Error:no results",urlmain,100,'','',str(page+1))
                        
               
               
      


               
def getmatch(match):
                if len(match)<1:
                        return
                for href in match:
                    
                    
                    
                    
                     
                    server=href.split("/")[2].replace('www.',"").replace("embed.","").split(".")[0]
                    #if 'hqq' in server or "myvi" in server or 'videomeh' in server:
                            #return
                    addDir(server,href,7,'')
def getHostName( url, nameOnly = False):
        hostName = ''
        match = re.search('https?://(?:www.)?(.+?)/', url)
        if match:
            hostName = match.group(1)
            if (nameOnly):
                n = hostName.split('.')
                hostName = n[-2]
       
        return hostName            		
        
def get_servers(url):
	        data=read_url(url)
	       
                	
                #regx='''</span><a href='(.+?)' class='redirect_link'>'''
                #regx1='''<iframe src="(.+?)" scrolling="no" frameborder="0" width="700" height="430" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'''
                regx2='''<li><a href="(.+?)" target=_blank>\n<img src="(.+?)" ></img>'''
                #regx2='<a href="http://www.youtube2.org/online/?p=785&url=http://vidbull.com/embed-zbdm3g7mfwe8-720x405.html" target=_blank>'

                
                regx3='''<iframe .+? src="(.+?)" .+?></iframe>'''
                regx4='''<iframe .+? src="(.+?)" ></iframe>'''
                regx1='''<source type="video/mp4" src="(.+?)" /><a'''
                #regx5='''<IFRAME .+? SRC="(.+?)" .+?></IFRAME>'''
                regx='''<a href="http://aflamy.pw/portal/(.+?)">'''
                try:newurl ="http://aflamy.pw/portal/"+ re.findall(regx,data, re.M|re.I)[0]
                except:newurl=url
                if newurl:
                   
                   data=read_url(newurl)
                   
                   regx='''<iframe src="(.+?)".+?></iframe>'''
                   regx='''<iframe.+?src="(.+?)".+?></iframe>'''
                   try:
                     links=re.findall(regx,data, re.M|re.I)
                     for link in links:  
                        if 'youtube'  in link:
                            continue
                        if 'facebook'  in link:
                            continue
                        server=getHostName(link)                    
                        addDir(server,link,7,'')
                   except:
                           pass

                        
                   try:      
                    
                    regx='''href="https://openload.co/f/(.+?)">'''
                    stream_url="https://openload.co/f/"+re.findall(regx,data, re.M|re.I)[0]
                    server=getHostName(stream_url)                    
                    addDir(server,stream_url,7,'')
                   except:
                           pass
                   try:     
                      regx='''<a target="_blank" href="http://uptobox.com/(.+?)">'''
                      stream_url="http://uptobox.com/"+re.findall(regx,data, re.M|re.I)[0]
                      server=getHostName(stream_url)                    
                      addDir(server,stream_url,7,'')
                   except:
                           pass
                  
                   try:     
                      regx='''src=".+?//www.dailymotion.com/embed/video/(.+?)">'''
                      stream_url="http://www.dailymotion.com/embed/video/"+re.findall(regx,data, re.M|re.I)[0]
                      server=getHostName(stream_url)                    
                      addDir(server,stream_url,7,'')
                   except:
                           pass




    

    
    
def resolve_host(url):##for xbmc version
    import urlresolver
    #hosted_media = urlresolver.HostedMediaFile(url=url, title="host")
    stream_link = urlresolver.resolve(url)
    print "stream_link",stream_link
    if stream_link is None or 'unresolvable' in stream_link:
            addDir("Error:links not found",url,2, '','')
            return
    xbmc.Player().play(stream_link)
    sys.exit(0)
    
def get_hostlink(url):
	        data=read_url2(url)
                
		
                regx='''<iframe src="(.+?)" width='''
                match = re.findall(regx,data, re.M|re.I)
                print 'match-mfaraj',match,url
                if len(match)<1:
                        regx="'proxy.link'.+?'(.+?)'"
                        match = re.findall(regx,data, re.M|re.I)
                        print 'match-mfaraj2',match,url
                        
                i=0
                for href in match:
                    
     
                    i=i+1
                    server='link1'+str(i)
                    addLink(server,href,7,'')



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
                                
        return param

def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok
	


def addDir(name,url,mode,iconimage,page=1):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def playlink(url):
            print "m2",url
	    listItem = xbmcgui.ListItem(path=str(url))
	    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)

              
params=get_params()
url=None
name=None
mode=None
initial=None
max=None
rating=None
cast=None
year=None
genre=None
duration=None
writer=None
director=None

	
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
        page=1


		


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "page: "+str(page)
if mode==None or url==None or len(url)<1:
        print ""
        getCategories()
       
elif mode==1:
        print ""+url
        getVideos(name,url,page)
elif mode==11:
        print ""+url
        getVideos(name,url,page)
        
  
elif mode==8:
        print ""+url        
        getblock(name,url,page)
        
        
elif mode==2:
        print ""+url
        get_servers(url)
        


elif mode==13:
        print ""+url
        search(url)		


elif mode==4:
        print ""+url
        get_servers2(url)
        
elif mode==5:
        print ""+url        
        
        GENRES(url)

elif mode==6:
        print ""+url
        get_hostlink(url)
elif mode==7:
        resolve_host(url)
        
elif mode==40:
        playlink(url)        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
