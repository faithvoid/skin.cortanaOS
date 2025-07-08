import os
import xbmc
import xbmcgui

OS_FILE = xbmc.translatePath('special://skin/scripts/utilities/os.txt')

def read_os_list():
    if os.path.exists(OS_FILE):
        with open(OS_FILE, "r") as f:
            return [line.strip().split(";") for line in f.readlines() if os.path.exists(line.strip().split(";")[0])]
    return []

def write_os_list(os_list):
    with open(OS_FILE, "w") as f:
        f.write("\n".join([";".join(entry) for entry in os_list]))

def browse_for_xbe():
    dialog = xbmcgui.Dialog()
    xbe_path = dialog.browse(1, "Select otherOS", "files", ".xbe", False, False, "E:\\")
    if xbe_path and os.path.exists(xbe_path):
        return xbe_path
    return None

def launch_xbe(xbe_path):
    xbmc.executebuiltin("RunXBE(" + xbe_path + ")")

def get_os_name():
    keyboard = xbmc.Keyboard("", "Enter OS name")
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    return None

def main():
    os_list = read_os_list()
    options = [entry[1] for entry in os_list] + ["Remove otherOS", "Install otherOS"]
    dialog = xbmcgui.Dialog()
    choice = dialog.select("otherOS", options)
    
    if choice == -1:
        return
    elif choice == len(os_list):
        remove_choice = dialog.select("Select otherOS to remove", [entry[1] for entry in os_list])
        if remove_choice != -1:
            del os_list[remove_choice]
            write_os_list(os_list)
            dialog.ok("otherOS", "otherOS has been successfully removed.")
    elif choice == len(os_list) + 1:
        xbe_path = browse_for_xbe()
        if xbe_path:
            os_name = get_os_name()
            if os_name:
                os_list.append([xbe_path, os_name])
                write_os_list(os_list)
                dialog.ok("otherOS", "Success! otherOS has been successfully added.")
                if dialog.yesno("otherOS", "Would you like to launch it now?"):
                    launch_xbe(xbe_path)
    else:
        launch_xbe(os_list[choice][0])

if __name__ == "__main__":
    main()
