import xbmc
import xbmcgui
import os

def read_browser_path():
    path = xbmc.getInfoLabel('Skin.String(Browser)')
    if path and os.path.exists(path):
        return path
    return None

def write_browser_path(path):
    xbmc.executebuiltin('Skin.SetString(Browser,%s)' % path)

def browse_for_xbe():
    dialog = xbmcgui.Dialog()
    xbe_path = dialog.browse(1, "Browser", "files", ".xbe", False, False, "E:\\")
    if xbe_path and os.path.exists(xbe_path):
        return xbe_path
    return None

def launch_xbe(xbe_path):
    xbmc.executebuiltin("RunXBE(%s)" % xbe_path)

def main():
    dialog = xbmcgui.Dialog()
    xbe_path = read_browser_path()
    if xbe_path:
        launch_xbe(xbe_path)
    else:
        if dialog.yesno("Browser", "Browser is not set.", "Would you like to add it now?"):
            xbe_path = browse_for_xbe()
            if xbe_path:
                write_browser_path(xbe_path)
                if dialog.yesno("Success!", "Browser has been set.", "Would you like to launch it now?"):
                    launch_xbe(xbe_path)

if __name__ == "__main__":
    main()
