import os
import xbmc
import xbmcgui

LOGIN_FILE = xbmc.translatePath('special://home/userdata/profiles/{}/login.txt'.format(xbmc.getInfoLabel('System.ProfileName')))

def get_user_input(heading, default_text=""):
    keyboard = xbmc.Keyboard(default_text, heading)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    return None

def save_login(username, password):
    try:
        with open(LOGIN_FILE, "w") as f:
            f.write(username + "\n")
            f.write(password)
        xbmcgui.Dialog().ok("Success", "cortanaChat login details saved successfully.")
    except Exception as e:
        xbmcgui.Dialog().ok("Error", "Failed to save login: " + str(e))

def load_login():
    try:
        with open(LOGIN_FILE, "r") as f:
            lines = f.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()
    except:
        pass
    return None, None

def main():
    username, password = None, None

    if os.path.exists(LOGIN_FILE):
        username, password = load_login()
        if username and password:
            choice = xbmcgui.Dialog().yesno(
                "cortanaChat - Login Found", 
                "{}".format(username), 
                "Would you like to edit your account information?"
            )
            if not choice:
                return
    else:
        choice = xbmcgui.Dialog().yesno(
            "cortanaChat", 
            "Login Not Found", 
            "Would you like to log in to cortanaChat (powered by Bluesky)?"
        )
        if not choice:
            return

    new_username = get_user_input("Enter Username", username if username else "")
    if new_username is None:
        return

    new_password = get_user_input("Enter App Password", password if password else "")
    if new_password is None:
        return

    save_login(new_username, new_password)

if __name__ == "__main__":
    main()
