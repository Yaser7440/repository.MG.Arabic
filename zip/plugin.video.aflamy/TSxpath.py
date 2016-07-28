import os
import sys

import sys,traceback
from os import listdir as os_listdir
TSmedia_error_file='/tmp/TSmedia_error'
print "TSxpath:adding TSmedia directories to system path......"
scripts = "/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts"
if os.path.exists(scripts):
   for name in os_listdir(scripts):
       if "script." in name:
               fold = scripts + "/" + name + "/lib"
               sys.path.append(fold)

TSmediaaddons="/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons"
sys.path.append(TSmediaaddons)
TSmediaresources="/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/resources"
sys.path.append(TSmediaresources)
print "TSxpath:Finished adding  TSmedia directories to system path......"
#############################################
def trace_error():
                  
                  traceback.print_exc(file = sys.stdout)
                  import os
                 
                  traceback.print_exc(file=open(TSmedia_error_file,"w"))


try:
    print "TSxpath:executing addon default......"
    
    sys.argv[0]=sys.argv[0].replace("TSxpath.py","default.py")
    sys.modules["__main__"].__file__=sys.argv[0]
    print "sys.argv-xpath",sys.argv
    
    import default
except:
    trace_error()   