import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,shutil,urllib2,urllib,re,extract,downloader,time,socket,net,speedtest
import pyxbmct.addonwindow as pyxbmct

net                     = net.Net()
addon_id                = 'plugin.video.MGwizard'
ADDON                   = xbmcaddon.Addon(id=addon_id)
selfAddon               = xbmcaddon.Addon(id=addon_id)
datapath                = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
packagespath            = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
icon                    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart                  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
fanart2                 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'fanart2.jpg'))
speedsplash             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'speedtest.png'))
fanart_tools            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'fanart_tools9.jpg'))
button_focus            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_focus.png'))
button_no_focus         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_no_focus.png'))
button_install_no_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_install_no_focus.png'))
button_install_focus    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_install_focus3.png'))
arrowup                 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'arrowup2.png'))
arrowdown               = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'arrowdown2.png'))
dialog                  = xbmcgui.Dialog()

## Create Window (title)
window          = pyxbmct.AddonDialogWindow('[COLOR red] MG Arabic Wizard [/COLOR]')# Create Window (title)

def MG():
    ## set globals so can be referenced anywhere in code
    global BuildsButton
    global WorldAddons
    
    
    global ToolsButton
    global CloseButton
    global InstallButton
    global MGlist
    global MGthumb
    global fan
    global InstallButton2
    global worldlist
    global buildtextbox
    global comlist
    global comlist2
    global ClearCache
    global Packages
    global SpeedTest
    global FreshStart
    global cachetextbox
    global packagestextbox
    global iptextbox
    global speedthumb
    global buildsgoup
    global buildsgoup 
    global worldgoup
    
   
    global toolsgoup 

    ## windows
    window.setGeometry(1240, 650, 100, 50)# Create Window (width,height,rows,cols)
    fan=pyxbmct.Image(fanart2)
    window.placeControl(fan, 0, 0, 101, 51)

    ## controls
    BuildsButton= pyxbmct.Button('MG Wizard',focusTexture=button_focus,noFocusTexture=button_no_focus)
    WorldAddons = pyxbmct.Button('MG Addons',focusTexture=button_focus,noFocusTexture=button_no_focus)
    
    
    ToolsButton = pyxbmct.Button('Tools',focusTexture=button_focus,noFocusTexture=button_no_focus)
    CloseButton = pyxbmct.Button('Close',focusTexture=button_focus,noFocusTexture=button_no_focus)
    InstallButton = pyxbmct.Button('[B]Install[/B]',focusTexture=button_install_focus,noFocusTexture=button_install_no_focus)
    MGlist = pyxbmct.List(buttonFocusTexture=button_focus)
    MGthumb=pyxbmct.Image(icon)
    worldlist = pyxbmct.List(buttonFocusTexture=button_focus)
    comlist = pyxbmct.List(buttonFocusTexture=button_focus)
    comlist2 = pyxbmct.List(buttonFocusTexture=button_focus)
    buildtextbox = pyxbmct.Label('',textColor='0xFFFFFFFF')
    ClearCache = pyxbmct.Button('Clear Cache',focusTexture=button_focus,noFocusTexture=button_no_focus)
    Packages = pyxbmct.Button('Delete Packages',focusTexture=button_focus,noFocusTexture=button_no_focus)
    SpeedTest = pyxbmct.Button('Internet Speed',focusTexture=button_focus,noFocusTexture=button_no_focus)
    FreshStart = pyxbmct.Button('KODI Factory Reset',focusTexture=button_focus,noFocusTexture=button_no_focus)
    cachetextbox = pyxbmct.Label('[COLOR red]Not Done[/COLOR]', alignment=pyxbmct.ALIGN_CENTER)
    packagestextbox = pyxbmct.Label('', alignment=pyxbmct.ALIGN_CENTER)
    iptextbox = pyxbmct.Label('', alignment=pyxbmct.ALIGN_CENTER)
    speedthumb=pyxbmct.Image(speedsplash)
    buildsgoup=pyxbmct.Image(arrowup) 
    worldgoup=pyxbmct.Image(arrowup)
 
    
    toolsgoup=pyxbmct.Image(arrowup) 

    ## control placement
    window.placeControl(BuildsButton,102, 3,  15, 9)
    window.placeControl(WorldAddons,102, 12, 15, 9)
    
    
    window.placeControl(ToolsButton,102, 30, 15, 9)
    window.placeControl(CloseButton,102, 39, 15, 9)
    window.placeControl(InstallButton,55, 26, 19, 5)
    window.placeControl(MGlist, 55, 1, 50, 15)
    window.placeControl(MGthumb, 38, 35, 55, 15)
    window.placeControl(worldlist, 38, 1, 60, 15)
    window.placeControl(comlist, 38, 1, 60, 15)
    window.placeControl(comlist2, 38, 1, 60, 15)
    window.placeControl(buildtextbox, 61, 16, 50, 10)
    window.placeControl(ClearCache,35, 3, 8, 9)
    window.placeControl(FreshStart,35, 15, 8, 9)
    window.placeControl(SpeedTest,35, 27, 8, 9)
    window.placeControl(Packages,35, 39, 8, 9)
    window.placeControl(cachetextbox, 42, 3, 8, 9)
    window.placeControl(packagestextbox, 42, 39, 8, 9)
    window.placeControl(iptextbox, 43, 15, 8, 22)
    window.placeControl(speedthumb, 54, 10, 43, 30)
    window.placeControl(buildsgoup, 99, 4, 4, 7)
    window.placeControl(worldgoup, 99, 13, 4, 7)

    
    window.placeControl(toolsgoup, 99, 31, 4, 7)

    ## control actions
    window.connect(BuildsButton, MGARABIC)
    window.connect(WorldAddons, WORLDADDONS)
    
    
    window.connect(ToolsButton, TOOLS)
    window.connect(CloseButton, window.close)
    window.connect(InstallButton, lambda:INSTALL(url))
    window.connect(ClearCache, DELETECACHE)
    window.connect(Packages, DELETEPACKAGES)
    window.connect(SpeedTest, SPEEDTEST)
    window.connect(FreshStart, RUNFRESHSTART)

    ## Event Lists
    window.setFocus(BuildsButton)
    window.connectEventList(
	[pyxbmct.ACTION_MOVE_DOWN,
	pyxbmct.ACTION_MOVE_UP,
        pyxbmct.ACTION_MOUSE_MOVE],
	MGLIST_UPDATE)

    ## Main Navigation
    BuildsButton.controlRight(WorldAddons)
    BuildsButton.controlLeft(CloseButton)
    WorldAddons.controlLeft(BuildsButton)
    ToolsButton.controlRight(CloseButton)
    CloseButton.controlRight(BuildsButton)
    CloseButton.controlLeft(ToolsButton)
    HIDEALL()
    
def HIDEALL():
    InstallButton.setVisible(False)
    MGlist.setVisible(False)
    MGthumb.setVisible(False)
    worldlist.setVisible(False)
    comlist.setVisible(False)
    comlist2.setVisible(False)
    buildtextbox.setVisible(False)
    ClearCache.setVisible(False)
    Packages.setVisible(False)
    SpeedTest.setVisible(False)
    FreshStart.setVisible(False)
    cachetextbox.setVisible(False)
    packagestextbox.setVisible(False)
    iptextbox.setVisible(False)
    speedthumb.setVisible(False)
    buildsgoup.setVisible(False)
    worldgoup.setVisible(False)
    
    
    toolsgoup.setVisible(False)
    
def SPEEDTEST():
    speed = speedtest.speedtest()
    speedthumb.setImage(speed[0])
      
def TOOLS():
    HIDEALL()
    fan.setImage(fanart_tools)
    ClearCache.setVisible(True)
    Packages.setVisible(True)
    SpeedTest.setVisible(True)
    FreshStart.setVisible(True)
    cachetextbox.setVisible(True)
    packagestextbox.setVisible(True)
    iptextbox.setVisible(True)
    speedthumb.setVisible(True)
    toolsgoup.setVisible(True)
    packages=GETFOLDERSIZE(packagespath)
    packagestextbox.setLabel(packages)
    inc=1
    match=re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(net.http_GET('http://www.iplocation.net/').content)
    for ip, region, country, isp in match:
        if inc <2:
            ipstring = '[COLOR red]Your IP Address is: '+ip+'\n'+'Your IP is based in: '+country+'[/COLOR]'
            iptextbox.setLabel(ipstring)
        inc=inc+1
    ToolsButton.controlUp(ClearCache)
    ClearCache.controlDown(ToolsButton)
    ClearCache.controlLeft(Packages)
    ClearCache.controlRight(FreshStart)
    FreshStart.controlDown(ToolsButton)
    FreshStart.controlLeft(ClearCache)
    FreshStart.controlRight(SpeedTest)
    SpeedTest.controlDown(ToolsButton)
    SpeedTest.controlLeft(FreshStart)
    SpeedTest.controlRight(Packages)
    Packages.controlDown(ToolsButton)
    Packages.controlLeft(SpeedTest)
    Packages.controlRight(ClearCache)
    

    

    
def MGARABIC():
    HIDEALL()
    fan.setImage(fanart)
    MGlist.reset()
    MGlist.setVisible(True)
    MGthumb.setVisible(True)
    InstallButton.setVisible(True)
    worldlist.setVisible(False)
    buildtextbox.setVisible(True)
    buildsgoup.setVisible(True)
    MGthumb.setImage(icon)
    link = net.http_GET('https://copy.com/SwKjJnQaTBd63NZa/wizard.txt?download=1').content.replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)"').findall(link)
    for name in match:
        name = '[COLOR red]'+name+'[/COLOR]'
        if 'MG' in name:
            MGlist.addItem(name)      
    BuildsButton.controlUp(MGlist)
    MGlist.controlDown(BuildsButton)
    MGlist.controlLeft(BuildsButton)

def WORLDADDONS():# after button click
    HIDEALL()
    fan.setImage(fanart)
    worldlist.reset()
    worldlist.setVisible(True)
    MGthumb.setVisible(True)
    InstallButton.setVisible(True)
    buildtextbox.setVisible(True)
    worldgoup.setVisible(True)
    MGthumb.setImage(icon)
    link = net.http_GET('https://copy.com/fVTVDkgpr8K4zlCY/addon_data.txt?download=1').content.replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)"').findall(link)
    for name in match:
        name = '[COLOR red]'+name+'[/COLOR]'
        worldlist.addItem(name)
    WorldAddons.controlUp(worldlist)
    worldlist.controlDown(WorldAddons)
    worldlist.controlLeft(WorldAddons)
      
def MGLIST_UPDATE():
  global url  
  try:
    if window.getFocus() == MGlist:
        pos=MGlist.getSelectedPosition()
        link = net.http_GET('https://copy.com/SwKjJnQaTBd63NZa/wizard.txt?download=1').content.replace('\n','').replace('\r','')
        MGimage = re.compile('img="(.+?)"').findall(link)[pos]
        MGthumb.setImage(MGimage)
        url = re.compile('url="(.+?)"').findall(link)[pos]
        name = re.compile('name="(.+?)"').findall(link)[pos]
        buildtextbox.setLabel(name)
        MGlist.controlRight(InstallButton)#Specific Window Control
        InstallButton.controlLeft(MGlist)#Specific Window Control
    elif window.getFocus() == worldlist:
        pos=worldlist.getSelectedPosition()
        link = net.http_GET('https://copy.com/fVTVDkgpr8K4zlCY/addon_data.txt?download=1').content.replace('\n','').replace('\r','')
        worldimage = re.compile('img="(.+?)"').findall(link)[pos]
        MGthumb.setImage(worldimage)
        url = re.compile('url="(.+?)"').findall(link)[pos]
        name = re.compile('name="(.+?)"').findall(link)[pos]
        buildtextbox.setLabel(name)
        worldlist.controlRight(InstallButton)#Specific Window Control
        InstallButton.controlLeft(worldlist)#Specific Window Control
    elif window.getFocus() == comlist:
        pos=comlist.getSelectedPosition()
        link = net.http_GET('https://copy.com/SwKjJnQaTBd63NZa/wizard.txt?download=1').content.replace('\n','').replace('\r','')
        comimage = re.compile('img="(.+?)"').findall(link)[pos]
        MGthumb.setImage(comimage)
        url = re.compile('url="(.+?)"').findall(link)[pos]
        name = re.compile('name="(.+?)"').findall(link)[pos]
        buildtextbox.setLabel(name)
        comlist.controlRight(InstallButton)#Specific Window Control
        InstallButton.controlLeft(comlist)#Specific Window Control  
    elif window.getFocus() == comlist2:
        pos=comlist2.getSelectedPosition()
        name=com2name[pos]
        url=com2url[pos]
        thumb=com2thumb[pos]
        MGthumb.setImage(thumb)
        name = '[COLOR grey]'+name+'[/COLOR]'
        buildtextbox.setLabel(name)
        comlist2.controlRight(InstallButton)#Specific Window Control
        InstallButton.controlLeft(comlist2)#Specific Window Control
    else:pass
  except:pass

def INSTALL(url):
    ret = dialog.yesno('[COLOR red]MGwizard[/COLOR]', 'For A Successful Update','Ensure You Have Cleared Data First','Do You Wish To Continue?','Cancel','Continue')
    if ret == 1:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR red]MGwizard[/COLOR]","MGwizard is creating your custom view",'', 'Please Wait')
        lib=os.path.join(path, 'download.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib, dp)
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        dp.update(0,"", "[COLOR red]Applying MGwizard View[/COLOR]")
        extract.all(lib,addonfolder,dp)
        try:
            os.remove(lib)
        except:
            pass
        FORCECLOSE()
    else:quit()

def FORCECLOSE():
    FoundPlatform = PLATFORMQUERY()
    if FoundPlatform == 'osx':
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR red]MG[/COLOR]", "MG configuration prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif FoundPlatform == 'linux':
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR red]MG[/COLOR]", "MG configuration prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif FoundPlatform == 'android':
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        dialog.ok("[COLOR red]MG[/COLOR]", "MG configuration prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    elif FoundPlatform == 'windows':
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR red]MG[/COLOR]", "MG configuration prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")
    else: #ATV
        try: os.system('killall AppleTV')
        except: pass
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR red]MG[/COLOR]", "MG configuration prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")

def PLATFORMQUERY():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

def GETFOLDERSIZE(path):
    global total_files
    global total_size
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(path):
	for f in filenames:
		fp = os.path.join(dirpath, f)
		total_size += os.path.getsize(fp)
		total_files = total_files + 1
    total_size=float(total_size/1024)/float(1024)
    total_size=format(total_size, '.2f')
    total_size=str(total_size)+'mb'
    total_size = '[COLOR red]'+total_size+'[/COLOR]'
    return total_size

def RUNFRESHSTART():
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('[COLOR red]MG[/COLOR]', '[COLOR red]This Will Wipe your KODI Install[/COLOR]','[COLOR red]Do You Wish To Continue?[/COLOR]','','Cancel','Continue')
    if ret == 1:
        addonPath=xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
        addonPath=xbmc.translatePath(addonPath) 
        xbmcPath=os.path.join(addonPath,"..","..");
        xbmcPath=os.path.abspath(xbmcPath)
        for root, dirs, files in os.walk(xbmcPath,topdown=False):
            for name in files:
                try: os.remove(os.path.join(root,name))
                except:pass    
            for name in dirs:
                try: os.rmdir(os.path.join(root,name))
                except:pass
        dialog.ok('[COLOR red]MG[/COLOR]', '[COLOR red]Your KODI Install Has Been Wiped[/COLOR]', '[COLOR red]Please Quit KODI To Take Effect[/COLOR]')
    else:
        dialog.ok('[COLOR red]MG[/COLOR]', '[COLOR red]Factory Reset Cancelled[/COLOR]', '[COLOR red]Nothing Has Been Changed[/COLOR]')
        quit()

def DELETECACHE():
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    dialog = xbmcgui.Dialog()
    cachetextbox.setLabel('[COLOR red]Complete[/COLOR]')

def DELETEPACKAGES():
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))   
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)            
        if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                packagestextbox.setLabel('[COLOR red]Complete[/COLOR]')
        else: packagestextbox.setLabel('[COLOR red]Complete[/COLOR]')

MG()
window.doModal() 

