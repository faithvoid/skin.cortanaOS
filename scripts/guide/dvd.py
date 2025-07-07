import os
import xbmc
import xbmcgui

D_DRIVE = "D:\\" 

def launch_xbe():
    try:
        files = os.listdir(D_DRIVE)  # This will fail on audio CDs
        for file in files:
            if file.endswith('default.xbe'):
                xbe_path = os.path.join(D_DRIVE, file)
                xbmc.executebuiltin('RunXBE("%s")' % xbe_path)
                return True
    except:
        return False  # Likely an audio CD or unreadable disc
    return False

def play_dvd():
    xbmc.executebuiltin("XBMC.PlayDVD")

def eject_tray():
    xbmc.executebuiltin("XBMC.EjectTray")

def check_disc():
    dvd_label = xbmc.getInfoLabel("System.DVDLabel")
    has_disc = xbmc.getCondVisibility("System.HasMediaDVD")

    if dvd_label in ["Open", "Empty"]:
        eject_tray()
    elif has_disc:
        if launch_xbe():
            return
        play_dvd()  # If no default.xbe found, try playing DVD
    else:
        eject_tray()
        xbmcgui.Dialog().ok(
            "Unrecognized Disc",
            "The disc is missing or unreadable.",
            "1. Clean the disc with a soft cloth and / or reinsert it.",
            "2. Restart the console."
        )

if __name__ == "__main__":
    check_disc()
