# -*- coding: utf-8 -*-
import xbmc
import xml.etree.ElementTree as ET
import urllib2
import re
from datetime import datetime, timedelta

def get_news_insignia(feed_url):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        for item in root.findall(".//item"):
            desc_elem = item.find("description")
            if desc_elem is not None and desc_elem.text:
                news_text = desc_elem.text.strip()
                # Safely wrap the value in quotes and escape internal ones
                safe_text = news_text.replace('"', "'")
                xbmc.executebuiltin('Skin.SetString(cortanaLatestNewsInsignia, "{}")'.format(safe_text))
                return True
    except Exception as e:
        xbmc.log("Error fetching or parsing news: %s" % str(e), xbmc.LOGERROR)
    return False

def get_news_xlink(feed_url):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        for item in root.findall(".//item"):
            desc_elem = item.find("description")
            if desc_elem is not None and desc_elem.text:
                news_text = desc_elem.text.strip()
                # Safely wrap the value in quotes and escape internal ones
                safe_text = news_text.replace('"', "'")
                xbmc.executebuiltin('Skin.SetString(cortanaLatestNewsXLink, "{}")'.format(safe_text))
                return True
    except Exception as e:
        xbmc.log("Error fetching or parsing news: %s" % str(e), xbmc.LOGERROR)
    return False

def get_news_cortana(feed_url):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        for item in root.findall(".//item"):
            desc_elem = item.find("description")
            if desc_elem is not None and desc_elem.text:
                news_text = desc_elem.text.strip()
                # Safely wrap the value in quotes and escape internal ones
                safe_text = news_text.replace('"', "'")
                xbmc.executebuiltin('Skin.SetString(cortanaLatestNewsCortana, "{}")'.format(safe_text))
                return True
    except Exception as e:
        xbmc.log("Error fetching or parsing news: %s" % str(e), xbmc.LOGERROR)
    return False


def get_event(feed_url, _unused_day_label=None):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        now = datetime.now()
        events = []

        def parse_day_label(day_label):
            cleaned_label = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', day_label)
            try:
                return datetime.strptime(cleaned_label, "%a, %b %d").date().replace(year=now.year)
            except Exception as e:
                xbmc.log("Failed to parse day label '{}': {}".format(day_label, e), xbmc.LOGERROR)
                return None

        for item in root.findall(".//item"):
            title_elem = item.find("title")
            desc_elem = item.find("description")

            if title_elem is None or desc_elem is None:
                continue

            title = title_elem.text.strip()
            description = desc_elem.text.strip()

            if not title.startswith("Game Event - "):
                continue

            title_match = re.match(r"Game Event - ([^:]+):\s*(.+)", title)
            if not title_match:
                continue
            day_label, game_name = title_match.groups()
            day_label = day_label.strip()
            game_name = game_name.strip()

            time_match = re.search(r"at (\d{1,2}:\d{2} (?:AM|PM) EST)", description)
            time_str = time_match.group(1) if time_match else "Time N/A"

            try:
                event_time = datetime.strptime(time_str, "%I:%M %p EST").time()

                if day_label.lower() == "today":
                    event_date = now.date()
                elif day_label.lower() == "tomorrow":
                    event_date = (now + timedelta(days=1)).date()
                else:
                    event_date = parse_day_label(day_label)
                    if event_date is None:
                        continue

                event_dt = datetime.combine(event_date, event_time)
            except Exception as e:
                xbmc.log("Failed to parse event time '{}': {}".format(time_str, e), xbmc.LOGERROR)
                continue

            label = "{}: {} ({})".format(day_label, game_name, time_str)
            events.append((event_dt, label))

        events.sort(key=lambda x: x[0])

        top_events = events[:3]

        return "[CR]".join([e[1] for e in top_events])

    except Exception as e:
        xbmc.log("Error extracting upcoming events: {}".format(str(e)), xbmc.LOGERROR)
    return ""

def main():

    insignia_url = "https://ogxbox.org/rss/insignia.xml"
    xlinkkai_url = "https://ogxbox.org/rss/xlinkkai.xml"

    get_news_cortana("http://faithvoid.github.io/cortana/news.xml")
    get_news_insignia("https://bsky.app/profile/did:plc:w72idvo677kghtpacp52gw4o/rss")
    get_news_xlink("https://bsky.app/profile/did:plc:u2xruus6ilpnxj7dk4ily6m6/rss")

    event_insignia = get_event(insignia_url)
    event_xlink = get_event(xlinkkai_url)

    if event_insignia:
        xbmc.executebuiltin('Skin.SetString(insigniaEvents, "{}")'.format(event_insignia))
    if event_xlink:
        xbmc.executebuiltin('Skin.SetString(xlinkEvents, "{}")'.format(event_xlink))

if __name__ == '__main__':
    main()
