# -*- coding: utf-8 -*-
import xbmc
import xml.etree.ElementTree as ET
import urllib2
import re

def get_news_insignia(feed_url):
    try:
        response = urllib2.urlopen(feed_url, timeout=10)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        for item in root.findall(".//item"):
            desc_elem = item.find("description")
            if desc_elem is not None and desc_elem.text:
                news_text = desc_elem.text.strip()
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
                safe_text = news_text.replace('"', "'")
                xbmc.executebuiltin('Skin.SetString(cortanaLatestNewsCortana, "{}")'.format(safe_text))
                return True
    except Exception as e:
        xbmc.log("Error fetching or parsing news: %s" % str(e), xbmc.LOGERROR)
    return False


def main():

    get_news_cortana("http://faithvoid.github.io/cortana/news.xml")
    get_news_insignia("https://bsky.app/profile/did:plc:w72idvo677kghtpacp52gw4o/rss")
    get_news_xlink("https://bsky.app/profile/did:plc:u2xruus6ilpnxj7dk4ily6m6/rss")

if __name__ == '__main__':
    main()
