import xbmc
import xbmcgui
import os

def read_vc_path():
    path = xbmc.getInfoLabel('Skin.String(VideoChat)')
    if path and os.path.exists(path):
        return path
    return None

def write_vc_path(path):
    xbmc.executebuiltin('Skin.SetString(VideoChat,%s)' % path)

def browse_for_xbe():
    dialog = xbmcgui.Dialog()
    xbe_path = dialog.browse(1, "Xbox Video Chat", "files", ".xbe", False, False, "E:\\")
    if xbe_path and os.path.exists(xbe_path):
        return xbe_path
    return None

def launch_xbe(xbe_path):
    xbmc.executebuiltin("RunXBE(%s)" % xbe_path)

def main():
    dialog = xbmcgui.Dialog()
    xbe_path = read_vc_path()
    if xbe_path:
        launch_xbe(xbe_path)
    else:
        if dialog.yesno("Xbox Video Chat", "Xbox Video Chat is not installed.", "Would you like to add it now?"):
            xbe_path = browse_for_xbe()
            if xbe_path:
                write_vc_path(xbe_path)
                if dialog.yesno("Success!", "Xbox Video Chat has been installed.", "Would you like to launch it now?"):
                    launch_xbe(xbe_path)

if __name__ == "__main__":
    main()
