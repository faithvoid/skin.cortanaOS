import xbmc
import xbmcgui
import urllib
import urllib2
import os
import json

QR_DIR = xbmc.translatePath("special://skin/media/QR")
if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR)

def generate_qr(data_url, image_path, color1, color2):
    qr_api_url = "https://api.qrcode-monkey.com/qr/custom"
    qr_data = {
        "data": data_url,
        "config": {
            "body": "square",
            "eye": "frame0",
            "eyeBall": "ball0",
            "gradientColor1": color1,
            "gradientColor2": color2,
            "gradientType": "linear",
            "gradientOnEyes": True
        },
        "size": 128,
        "download": False,
        "file": "png"
    }

    qr_data_encoded = json.dumps(qr_data)

    try:
        request = urllib2.Request(qr_api_url, data=qr_data_encoded)
        request.add_header("Content-Type", "application/json")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
        request.add_header("Referer", "https://www.qrcode-monkey.com/")
        request.add_header("Accept", "application/json")

        response = urllib2.urlopen(request)

        with open(image_path, "wb") as f:
            f.write(response.read())

    except urllib2.HTTPError as e:
        xbmc.executebuiltin('Notification(cortanaOS, HTTP Error {}, 3000)'.format(e.code))
    except Exception as e:
        xbmc.executebuiltin('Notification(cortanaOS, Error downloading QR Code: {}, 3000)'.format(str(e)))

def generate_current_ip_qr():
    ip_address = xbmc.getInfoLabel("Network.IPAddress")
    if not ip_address or ip_address == "0.0.0.0":
        xbmc.executebuiltin('Notification(cortanaOS, Failed to retrieve current IP address., 3000, error)')
        return

    formatted_ip = "ftp://xbox@" + ip_address
    image_path = os.path.join(QR_DIR, "IP.png")
    generate_qr(formatted_ip, image_path, "#5f6781", "#7099d2")

def generate_kai_ip_qr():
    ip_address = xbmc.getInfoLabel("Skin.String(KaiIP)").strip()

    if not ip_address or ip_address == "0.0.0.0":
        try:
            keyboard = xbmc.Keyboard('', 'Enter Kai IP Address')
            keyboard.doModal()
            if keyboard.isConfirmed():
                ip_address = keyboard.getText().strip()
                if not ip_address:
                    xbmc.executebuiltin('Notification(cortanaOS, No IP address entered., 3000, error)')
                    return
                xbmc.executebuiltin('Skin.SetString(KaiIP,{})'.format(ip_address))
            else:
                xbmc.executebuiltin('Notification(cortanaOS, Kai IP entry canceled., 3000, error)')
                return
        except Exception as e:
            xbmc.executebuiltin('Notification(cortanaOS, Keyboard input failed., 3000, error)')
            return

    formatted_ip = "http://" + ip_address + ":34522"
    image_path = os.path.join(QR_DIR, "KaiIP.png")
    generate_qr(formatted_ip, image_path, "#82BD80", "#547852")

generate_current_ip_qr()
generate_kai_ip_qr()

xbmc.executebuiltin('Notification(cortanaOS, QR codes generated successfully!, 3000, special://skin/media/QR/IP.png)')
