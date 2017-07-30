# -*- coding: utf8 -*-By. MG.Arabic http://mg.esy.es/Kodi/
import sys
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,xbmcvfs
import requests
#------------------------------
from md_request import get_params
from md_request import OPEN_URL
from md_request import decodeHtml
from md_request import gethostname
from md_request import resolve_host
from md_request import regex_get_all
from md_request import regex_from_to
from md_request import addDir
from md_request import addDir2
from md_request import addLink
from md_request import playlink
#------------------------------
from common import Addon
from md_view import setView
from addon.common.net import Net
#------------------------------


addon_id='plugin.video.arab-moviezorg'
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/img/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, art+'/icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , art+'/fanart.jpg'))
HOME   =  xbmc.translatePath('special://home/')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
baseurl = 'http://arab-moviez.org'
net = Net()

def decodeHtml(text):
    text = text.replace('free counter statistics','[B][COLOR red]••MG.Arabic••http://mg.esy.es/Kodi/••[/COLOR][/B]').replace('افلام','').replace('Top News','[B][COLOR red]••MG.Arabic••[/COLOR][/B]').replace('مباشرة','')
    text = text.replace('تحميل','').replace('..','').replace('عربية','').replace('لاين','').replace('اجنبية','')
    text = text.replace('اون','').replace('بدون تحميل','').replace('مشاهدة','').replace('مترجمة','').replace('مترجم','').replace('كرتون','').replace('&#8211;','').replace('&#038;','').replace('&#8217;','').replace(',','')
    text = text.replace('   ', '').replace('افلام','').replace('أجنبية','').replace('منوعة','')
    return text 
def decodeHtml2(text):
    text = text.replace('Top News','[B][COLOR red]••MG.Arabic••[/COLOR][/B]')
    return text




####functions
def read_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', 'arab-moviez.org')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
	return link
      
         

##########################################parsing tools
def CAT():
        #addDir('[B][COLOR white]البحث[/COLOR][/B]',baseurl+'?s=',103,icon,fanart,'')
        addDir('[B][COLOR white]افلام جديده[/COLOR][/B]',baseurl,100,icon,fanart,'')
        addDir('[B][COLOR red]Box Office[/COLOR][/B]',baseurl+'/boxoffice.php',100,icon,fanart,'')
        addDir('[B][COLOR white]قوائم الافلام[/COLOR][/B]',baseurl,4,icon,fanart,'')
        addDir('[B][COLOR white]افلام السنه[/COLOR][/B]',baseurl,6,icon,fanart,'')
        addDir('[B][COLOR white]عـــــــام[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR red]••MG.Arabic••http://mg.esy.es/Kodi/••[/COLOR][/B]','','',fanart,fanart,'')
        

def TV1ARALAB(url):
	    
		#addDir('SEARCH',baseurl+'?s=',103,icon,fanart)
		link = OPEN_URL(url)
	#try:
		menu=re.compile('<div class="navbar-coll(.+?)/ul>',re.DOTALL).findall(link)
		for url in menu:
			matchsections = re.compile('<a href="(.+?)".*?>(.+?)</a></li>').findall(url)
			for url,name in matchsections:
				url = url
				url = re.sub(' ','%20',url)
				addDir('[B][COLOR white]%s[/COLOR][/B]'%decodeHtml2(name),url,100,icon,fanart)
                addDir('[B][COLOR red]••MG.Arabic••http://mg.esy.es/Kodi/••[/COLOR][/B]','','',fanart,fanart)
def TV2ARALAB(url):
	    
		#addDir('SEARCH','?s=',102,icon,fanart)
		link = OPEN_URL(url)
	#try:
		menu=re.compile('<div class="yea(.+?)/ul>',re.DOTALL).findall(link)
		for url in menu:
			matchsections = re.compile('<a href="(.+?)".*?>(.+?)</a></li>').findall(url)
			for url,name in matchsections:
				url = url
				url = re.sub(' ','%20',url)
				addDir('[B][COLOR white]%s[/COLOR][/B]'%decodeHtml2(name),url,100,icon,fanart)
                addDir('[B][COLOR red]••MG.Arabic••http://mg.esy.es/Kodi/••[/COLOR][/B]','','',fanart,fanart)				
def TV3ARALAB(url):
	    
		#addDir2('SEARCH','url',23,icon,fanart)
		link = OPEN_URL(url)
	#try:
		menu=re.compile('<div class="footl(.+?)/div>',re.DOTALL).findall(link)
		for url in menu:
			matchsections = re.compile('<a.*?href="(.+?)">(.+?)</a>').findall(url)
			for url,name in matchsections:
				url = url
				url = re.sub(' ','%20',url)
				addDir('[B][COLOR white]%s[/COLOR][/B]'%decodeHtml2(name),url,100,icon,fanart)				
                addDir('[B][COLOR red]••MG.Arabic••http://mg.esy.es/Kodi/••[/COLOR][/B]','','',fanart,fanart)				
				
				
				
				
				
				
				
		

			 
        			 
###################################movies
			  
def search(url):
        
        
         
        search_entered = ''
        debug=True
        if debug:
               keyboard = xbmc.Keyboard(search_entered, 'Search ِAnakbNet')
               keyboard.doModal()
               if keyboard.isConfirmed():
                   search_entered = keyboard.getText() .replace(' ','+')  
                   
                   
        else:
             print "search error"
            
        
        
         
        url= url+search_entered
        
          
        getmovies("Search",url,0)


                        
               
                   
                
        
def getmovies(url):##movies
    link = OPEN_URL(url)
    #link = link.encode('ascii', 'ignore').decode('ascii')
    #addon.log('#######################link = '+str(link))
    all_videos = regex_get_all(link, '<ul class="img-list">', '<div class="file_index col-lg-3">')
    items = len(all_videos)
    for a in all_videos:
        name = regex_from_to(a, '<div class="video_typ2">', '</div>').replace('&#039;',"'").replace('&amp;',"&")
        url = regex_from_to(a, 'href="', '"').replace('&#039;',"'").replace('&amp;',"&")
        icon = regex_from_to(a, 'src="', '"').replace('&#039;',"'").replace('&amp;',"&")
        fanart = regex_from_to(a, 'src="', '"').replace('&#039;',"'").replace('&amp;',"&")        
        desc = regex_from_to(a, '<span class="category">\s*<a href=".*?>', '\s*</a>').replace('&#039;',"'").replace('&amp;',"&")
        genre =regex_from_to(a, '<div class="video_typ">\s*', '</div>').replace('<br />','').replace('&#039;',"'").replace('&amp;',"&")
        date = regex_from_to(a, '<span>لسنة</span><div class="desc_itrm">', '</div>').replace('<span>',"")
        credits = regex_from_to(a, 'alt="', '"').replace('&#039;',"'").replace('&amp;',"&")
        rat = regex_from_to(a, '<span>التقييم</span>\s*<div class="desc_itrm">', '</div>').replace('&#039;',"'").replace('&amp;',"&")
        addDir2('[B][COLOR white]%s[/COLOR][/B]'%name,url,1,icon,fanart,desc,genre,date,'',credits,rat,items)
    try:
        OPEN = OPEN_URL(url)
        Regex = re.compile('<div class="pagination">(.+?)<div align="center">',re.DOTALL).findall(OPEN)[0]
        Regex2 = re.compile('href="(.*?)">(.+?)</a>',re.DOTALL).findall(str(Regex))	
        for url,name in Regex2:
                    addDir('[B][COLOR red][%s] Page>>>[/COLOR][/B]'%name,url,100,art+'/next.png',fanart,'')
    except: pass
    setView(addon_id, 'movies', 'movie-view')
		   
				

                    

#######################################host resolving                                                    
def getmatch(match):
                if len(match)<1:
                        return
                for href in match:
                    
                    if not href.startswith("http"):
                       href="http:"+href
                    #href=href.replace("/f/","/embed/")
                    
                    
                     
                    server=href.split("/")[2].replace('www.',"").replace("embed.","").split(".")[0]
                    # if 'hqq' in server or "myvi" in server or 'videomeh' in server:
                            # return
                    addDir('[B][COLOR white][%s][/COLOR][/B]'%server,href,2,'')

        
def get_servers(name,urlmain):
                urlmain=urlmain.replace("/film/","/play/")
                data=read_url(urlmain)
	        print data
                	
                #regx='''</span><a href='(.+?)' class='redirect_link'>'''
                #regx1='''<iframe src="(.+?)" scrolling="no" frameborder="0" width="700" height="430" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'''
                #regx2='''<iframe width="640" height="400" src="(.*?)" frameborder="0" allowfullscreen></iframe>'''
                
                regx3='''<iframe.*?src="(.*?)".*?></iframe>'''
                #regx4='''<iframe src="(.*?)"></iframe>'''
                #regx5='''<IFRAME .+? SRC="(.+?)" .+?></IFRAME>'''
               
                #match1 = re.findall(regx1,data, re.M|re.I)
                #match2 = re.findall(regx2,data, re.M|re.I)
                match3 = re.findall(regx3,data, re.M|re.I)
                #match4 = re.findall(regx4,data, re.M|re.I)
                #match5 = re.findall(regx5,data, re.M|re.I)
         
                #getmatch(match1)
                #getmatch(match2)
                getmatch(match3)
                #getmatch(match4)
                #getmatch(match5)
               
                return

############################################xbmc tools	    


# def addLink5(name,url,mode,iconimage):
        
    # u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    # ok=True
    # liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    # liz.setInfo( type="Video", infoLabels={ "Title": name } )
    # liz.setProperty("IsPlayable","true");
    
    # ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    # return ok


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
site=None
query=None
type=None	
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
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
try:
        page=int(params["page"])
except:
	pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "iconimage: "+str(iconimage)
print "description: "+str(description)
print "query: "+str(query)
print "type: "+str(type)
print "page: "+str(page)

if mode==None or url==None or len(url)<1: CAT()
elif mode==4: TV1ARALAB(url)
elif mode==5: TV2ARALAB(url)
elif mode==6: TV3ARALAB(url)		
elif mode==1: get_servers(name,url)
elif mode==2: resolve_host(url)		     
elif mode==3: playlink(url)             
elif mode==100: getmovies(url)
elif mode==10: YEARSEN(name)		
elif mode==103: search(url)    

xbmcplugin.endOfDirectory(int(sys.argv[1]))                              































































































































































































































if xbmcvfs.exists(xbmc.translatePath('special://home/userdata/sources.xml')):
        with open(xbmc.translatePath('special://home/userdata/sources.xml'), 'r+') as f:
                my_file = f.read()
                if re.search(r'http://mg.esy.es/Kodi', my_file):
                        addon.log('===MG.Arabic===Source===Found===in===sources.xml===Not Deleting.===')
                else:
                        line1 = "you have Installed The MDrepo From An"
                        line2 = "Unofficial Source And Will Now Delete Please"
                        line3 = "Install From [COLOR red]http://mg.esy.es/Kodi[/COLOR]"
                        line4 = "Removed Repo And Addon"
                        line5 = "successfully"
                        xbmcgui.Dialog().ok(addon_name, line1, line2, line3)
                        delete_addon = xbmc.translatePath('special://home/addons/'+addon_id)
                        delete_repo = xbmc.translatePath('special://home/addons/repository.MG.Arabic')
                        shutil.rmtree(delete_addon, ignore_errors=True)
                        shutil.rmtree(delete_repo, ignore_errors=True)
                        dialog = xbmcgui.Dialog()
                        addon.log('===DELETING===ADDON===+===REPO===')
                        xbmcgui.Dialog().ok(addon_name, line4, line5)