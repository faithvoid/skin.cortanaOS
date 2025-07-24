# This will probably crash your Xbox. Don't say I didn't warn you! 
# -*- coding: utf-8 -*-
import xbmc
import xml.etree.ElementTree as ET
import urllib2

def fetch_feed_root(feed_url):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        return ET.fromstring(xml_data)
    except Exception as e:
        xbmc.log("Error fetching or parsing RSS feed '%s': %s" % (feed_url, str(e)), xbmc.LOGERROR)
        return None


def get_users_online(root):
    try:
        for item in root.findall(".//item"):
            title = item.find("title").text
            if title.startswith("Users Online:"):
                return int(title.split(":")[1].strip())
    except Exception as e:
        xbmc.log("Error extracting users online: %s" % str(e), xbmc.LOGERROR)
    return 0


def get_sessions(root):
    try:
        for item in root.findall(".//item"):
            title = item.find("title").text
            if title.startswith("Active Games:"):
                return int(title.split(":")[1].strip())
    except Exception as e:
        xbmc.log("Error extracting sessions: %s" % str(e), xbmc.LOGERROR)
    return 0


def main():
    insignia_url = "https://ogxbox.org/rss/insignia.xml"
    xlinkkai_url = "https://ogxbox.org/rss/xlinkkai.xml"

    while True:
        insignia_root = fetch_feed_root(insignia_url)
        xlink_root = fetch_feed_root(xlinkkai_url)

        if not insignia_root or not xlink_root:
            time.sleep(300)
            continue

        insignia_users = get_users_online(insignia_root)
        xlinkkai_users = get_users_online(xlink_root)
        insignia_sessions = get_sessions(insignia_root)
        xlinkkai_sessions = get_sessions(xlink_root)

        combined_string = "({} [Insignia] | {} [XLink Kai])".format(insignia_users, xlinkkai_users)
        insignia_string = "({} players)".format(insignia_users)
        xlink_string = "({} players)".format(xlinkkai_users)
        xlinksession_string = "({})".format(xlinkkai_sessions)
        insigniasession_string = "({})".format(insignia_sessions)

        xbmc.executebuiltin('Skin.SetString(cortanaOnlinePlayers, "{}")'.format(combined_string))
        xbmc.executebuiltin('Skin.SetString(cortanaOnlineInsignia, "{}")'.format(insignia_string))
        xbmc.executebuiltin('Skin.SetString(cortanaOnlineXLink, "{}")'.format(xlink_string))
        xbmc.executebuiltin('Skin.SetString(cortanaSessionsXLink, "{}")'.format(xlinksession_string))
        xbmc.executebuiltin('Skin.SetString(cortanaSessionsInsignia, "{}")'.format(insigniasession_string))

        xbmc.sleep(60000)

if __name__ == '__main__':
    main()
