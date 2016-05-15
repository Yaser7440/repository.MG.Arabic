import xbmc,xbmcaddon,xbmcgui,xbmcplugin

class WookieWindow(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self.caption = kwargs.get('caption','')
        self.text = kwargs.get('text','')
        xbmcgui.WindowXMLDialog.__init__(self)

    def onInit(self):
        self.getControl(100).setLabel(self.caption)
        self.getControl(200).setText(self.text)
