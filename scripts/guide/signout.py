import xbmc
import xbmcgui

def main():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno("Sign Out", "Are you sure you want to sign out?")

    if confirm:
        profile_name = xbmc.getInfoLabel("System.ProfileName")
        profile_thumb = xbmc.getInfoLabel("System.ProfileThumb")

        if not profile_thumb:
            profile_thumb = "DefaultUser.png"

        xbmc.executebuiltin('Notification(Signed Out, ' + profile_name + ' has signed out., 3000, ' + profile_thumb + ')')

        xbmc.executebuiltin("Close")
        xbmc.executebuiltin("System.LogOff")

if __name__ == '__main__':
    main()
