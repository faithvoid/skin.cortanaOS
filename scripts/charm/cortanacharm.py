import xbmc
import xbmcgui
import sys
import requests
import re
import os

def sanitize_for_fatx(name):
    sanitized = re.sub(r'[^A-Za-z0-9_-]', '_', name)
    return sanitized[:30]

def get_xbox_live_profile():
    try:
        # Ask user for Gamertag
        kb = xbmc.Keyboard('', 'Enter Xbox Live Gamertag')
        kb.doModal()
        if not kb.isConfirmed():
            return
        gamertag = kb.getText()

        if not gamertag:
            return

        # Query PlayerDB API
        url = "https://playerdb.co/api/player/xbox/" + gamertag.lower()
        response = requests.get(url)
        data = response.json()

        if data.get("code") == "player.found":
            profile = data["data"]["player"]["meta"]
            username = data["data"]["player"]
            gamerscore = profile.get("gamerscore", "0")
            reputation = profile.get("xboxOneRep", "GoodPlayer")
            accountTier = profile.get("accountTier", "Silver")
            cortanaID = username.get("username", "")
            avatar_url = username.get("avatar", "")

            # Map reputation to numeric string
            rep_map = {
                "GoodPlayer": "5",
                "NeedsWork": "3",
                "AvoidMe": "1"
            }
            rep_value = rep_map.get(reputation, "5")

            # Set skin string values
            xbmc.executebuiltin('Skin.SetString(gamerscore,%s)' % gamerscore)
            xbmc.executebuiltin('Skin.SetString(reputation,%s)' % rep_value)
            xbmc.executebuiltin('Skin.SetString(accountTier,%s)' % accountTier)
            xbmc.executebuiltin('Skin.SetString(cortanaID,%s)' % cortanaID)

            # Save avatar to Q:/SANITIZED_USERNAME.png
            if avatar_url and cortanaID:
                safe_name = sanitize_for_fatx(cortanaID)
                avatar_path = "Q:/%s.png" % safe_name
                try:
                    img_data = requests.get(avatar_url, verify=False).content
                    with open(avatar_path, 'wb') as f:
                        f.write(img_data)
                    xbmc.executebuiltin('Skin.SetString(avatarPath,%s)' % avatar_path)
                except Exception as e:
                    xbmcgui.Dialog().ok("cortanaCharm", "Failed to save avatar: %s" % str(e))

            xbmcgui.Dialog().ok("cortanaCharm", "Profile synchronized successfully!")
        else:
            xbmcgui.Dialog().ok("cortanaCharm", "Gamertag not found.")

    except Exception as e:
        xbmcgui.Dialog().ok("Error", "Failed to get profile: %s" % str(e))

valid_labels = ['cortanaID', 'Toggle Charms', 'Gamerscore', 'Zone', 'Reputation', 'Account Tier', 'Get from Xbox Live']

# Handle script arguments from skin or show menu
if len(sys.argv) > 1 and sys.argv[1] in valid_labels:
    label = sys.argv[1]
else:
    choice = xbmcgui.Dialog().select('cortanaCharm', valid_labels)
    if choice == -1:
        sys.exit()
    label = valid_labels[choice]

# Handle Xbox Live fetch separately
if label == 'Get from Xbox Live':
    get_xbox_live_profile()

elif label == 'Account Tier':
    tiers = ['Gold', 'Silver', 'Bronze', 'Green', 'Blue', 'Pink']
    choice = xbmcgui.Dialog().select('Select cortanaCharm Theme', tiers)
    if choice != -1:
        tier = tiers[choice]
        xbmc.executebuiltin('Skin.SetString(accountTier,%s)' % tier)

elif label == 'Zone':
    zones = ['Family', 'Recreation', 'Pro', 'Underground', 'Custom']
    choice = xbmcgui.Dialog().select('Select Zone', zones)
    if choice != -1:
        zone = zones[choice]
        if zone == 'Custom':
            kb = xbmc.Keyboard('', 'Enter Zone')
            kb.doModal()
            if kb.isConfirmed():
                custom_zone = kb.getText()
                if custom_zone:
                    xbmc.executebuiltin('Skin.SetString(zone,%s)' % custom_zone)
        else:
            xbmc.executebuiltin('Skin.SetString(zone,%s)' % zone)

elif label == 'Toggle Charms':
            xbmc.executebuiltin('Skin.ToggleSetting(charmIcons)')

else:
    kb = xbmc.Keyboard('', 'Enter %s' % label)
    kb.doModal()

    if kb.isConfirmed():
        value = kb.getText()
        if value:
            if label == 'cortanaID':
                xbmc.executebuiltin('Skin.SetString(cortanaID,%s)' % value)
            elif label == 'Gamerscore':
                xbmc.executebuiltin('Skin.SetString(gamerscore,%s)' % value)
            elif label == 'Reputation':
                xbmc.executebuiltin('Skin.SetString(reputation,%s)' % value)
