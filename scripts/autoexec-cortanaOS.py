import xbmc

# Only proceed if a network connection is detected
if xbmc.getCondVisibility("System.HasNetwork"):
    xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/serverbrowser/getnews.py)")
    xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/serverbrowser/playercount.py)")
    # xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/startup/mediapresence.py)")
    # xbmc.executebuiltin("XBMC.RunScript(special://skin/scripts/chat/notifier.py)")
else:
    xbmc.log("Network not available, skipping startup scripts.", xbmc.LOGNOTICE)
