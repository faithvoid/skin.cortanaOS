import os
import xbmc
import xbmcgui

VC_FILE = xbmc.translatePath('special://skin/scripts/chat/vc.txt')

def read_vc_path():
    if os.path.exists(VC_FILE):
        with open(VC_FILE, "r") as f:
            path = f.readline().strip()
            if os.path.exists(path):
                return path
    return None

def write_vc_path(path):
    with open(VC_FILE, "w") as f:
        f.write(path)

def browse_for_xbe():
    dialog = xbmcgui.Dialog()
    xbe_path = dialog.browse(1, "Xbox Video Chat", "files", ".xbe", False, False, "E:\\")
    if xbe_path and os.path.exists(xbe_path):
        return xbe_path
    return None

def launch_xbe(xbe_path):
    xbmc.executebuiltin("RunXBE(" + xbe_path + ")")

def main():
    xbe_path = read_vc_path()
    dialog = xbmcgui.Dialog()
    if xbe_path:
        launch_xbe(xbe_path)
    else:
        if dialog.yesno("Xbox Video Chat Not Found", "Xbox Video Chat is not installed or the path is missing.", "Would you like to add it now?"):
            xbe_path = browse_for_xbe()
            if xbe_path:
                write_vc_path(xbe_path)
                if dialog.yesno("Success!", "Xbox Video Chat path has been set.", "Would you like to launch it now?"):
                    launch_xbe(xbe_path)

if __name__ == "__main__":
    main()
