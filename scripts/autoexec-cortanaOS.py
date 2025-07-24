import xbmc

# Only proceed if a network connection is detected
if xbmc.getCondVisibility("System.HasNetwork"):
    xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/serverbrowser/getnews.py)") # Fetches Insignia & XLink Kai News & Events
    xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/serverbrowser/playercount.py)") # Fetches Insignia & XLink Kai player counts
    # xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/startup/sakuraMedia.py)") # Xbox Discord Rich Presence for media
    # xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/chat/notifier.py)") # cortanaChat notifications
else:
    xbmc.log("Network not available, skipping startup scripts.", xbmc.LOGNOTICE)
