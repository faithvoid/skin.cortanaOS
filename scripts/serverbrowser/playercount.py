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


def get_insignia_statistics(root):
    stats = {
        "users_online": None,
        "active_games": None,
        "registered_users": None,
        "games_supported": None
    }

    try:
        for item in root.findall(".//item"):
            title = item.find("title").text

            if title.startswith("Users Online:"):
                stats["users_online"] = title
            elif title.startswith("Registered Users:"):
                stats["registered_users"] = title
            elif title.startswith("Games Supported:"):
                stats["games_supported"] = title
            elif title.startswith("Active Games:"):
                stats["active_games"] = title

    except Exception as e:
        xbmc.log("Error parsing Insignia stats: %s" % str(e), xbmc.LOGERROR)

    return stats


def get_xlinkkai_statistics(root):
    stats = {
        "users_online": None,
        "users_today": None,
        "server_status": None,
        "supported_games": None,
        "total_users": None,
        "orbital_servers": None,
        "orbital_sync": None,
        "game_traffic": None,
        "orbital_traffic": None
    }

    try:
        for item in root.findall(".//item"):
            title = item.find("title").text

            if title.startswith("Users Online:"):
                stats["users_online"] = title
            elif title.startswith("Users Today:"):
                stats["users_today"] = title
            elif title.startswith("Server Status:"):
                stats["server_status"] = title
            elif title.startswith("Supported Games:"):
                stats["supported_games"] = title
            elif title.startswith("Total Users:"):
                stats["total_users"] = title
            elif title.startswith("Orbital Servers Online:"):
                stats["orbital_servers"] = title
            elif title.startswith("Orbital Mesh Sync:"):
                stats["orbital_sync"] = title
            elif title.startswith("Game Traffic:"):
                stats["game_traffic"] = title
            elif title.startswith("Orbital Server Traffic:"):
                stats["orbital_traffic"] = title

    except Exception as e:
        xbmc.log("Error parsing XLink Kai stats: %s" % str(e), xbmc.LOGERROR)

    return stats


def main():
    insignia_url = "https://ogxbox.org/rss/insignia.xml"
    xlinkkai_url = "https://ogxbox.org/rss/xlinkkai.xml"

    insignia_root = fetch_feed_root(insignia_url)
    xlink_root = fetch_feed_root(xlinkkai_url)

    if not insignia_root or not xlink_root:
        return

    insignia_users = get_users_online(insignia_root)
    xlinkkai_users = get_users_online(xlink_root)
    insignia_sessions = get_sessions(insignia_root)
    xlinkkai_sessions = get_sessions(xlink_root)

    combined_string_header = "- {} on Insignia, {} on XLink Kai -".format(insignia_users, xlinkkai_users)
    combined_string = "({} [Insignia] | {} [XLink Kai])".format(insignia_users, xlinkkai_users)
    insignia_string = "({} players)".format(insignia_users)
    xlink_string = "({} players)".format(xlinkkai_users)
    xlinksession_string = "({})".format(xlinkkai_sessions)
    insigniasession_string = "({})".format(insignia_sessions)

    xlink_stats = get_xlinkkai_statistics(xlink_root)
    insignia_stats = get_insignia_statistics(insignia_root)

    xbmc.executebuiltin('Skin.SetString(cortanaOnlinePlayers, "{}")'.format(combined_string))
    xbmc.executebuiltin('Skin.SetString(cortanaOnlinePlayersHeader, "{}")'.format(combined_string_header))
    xbmc.executebuiltin('Skin.SetString(cortanaOnlineInsignia, "{}")'.format(insignia_string))
    xbmc.executebuiltin('Skin.SetString(cortanaOnlineXLink, "{}")'.format(xlink_string))
    xbmc.executebuiltin('Skin.SetString(cortanaSessionsXLink, "{}")'.format(xlinksession_string))
    xbmc.executebuiltin('Skin.SetString(cortanaSessionsInsignia, "{}")'.format(insigniasession_string))
    xbmc.executebuiltin('Skin.SetString(insigniaUsersOnline, "{}")'.format(insignia_stats["users_online"]))
    xbmc.executebuiltin('Skin.SetString(insigniaRegisteredUsers, "{}")'.format(insignia_stats["registered_users"]))
    xbmc.executebuiltin('Skin.SetString(insigniaGamesSupported, "{}")'.format(insignia_stats["games_supported"]))
    xbmc.executebuiltin('Skin.SetString(insigniaActiveGames, "{}")'.format(insignia_stats["active_games"]))
    xbmc.executebuiltin('Skin.SetString(xlinkUsersOnline, "{}")'.format(xlink_stats["users_online"]))
    xbmc.executebuiltin('Skin.SetString(xlinkUsersToday, "{}")'.format(xlink_stats["users_today"]))
    xbmc.executebuiltin('Skin.SetString(xlinkServerStatus, "{}")'.format(xlink_stats["server_status"]))
    xbmc.executebuiltin('Skin.SetString(xlinkSupportedGames, "{}")'.format(xlink_stats["supported_games"]))
    xbmc.executebuiltin('Skin.SetString(xlinkTotalUsers, "{}")'.format(xlink_stats["total_users"]))
    xbmc.executebuiltin('Skin.SetString(xlinkOrbitalServers, "{}")'.format(xlink_stats["orbital_servers"]))
    xbmc.executebuiltin('Skin.SetString(xlinkOrbitalSync, "{}")'.format(xlink_stats["orbital_sync"]))
    xbmc.executebuiltin('Skin.SetString(xlinkGameTraffic, "{}")'.format(xlink_stats["game_traffic"]))
    xbmc.executebuiltin('Skin.SetString(xlinkOrbitalTraffic, "{}")'.format(xlink_stats["orbital_traffic"]))

if __name__ == '__main__':
    main()
