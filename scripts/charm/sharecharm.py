import xbmc
import xbmcgui
import time
import struct
import os
import re
import urllib2
import mimetypes
import uuid
import urllib
import shutil
import json

MEDIA_PATH = "F:\\Media\\"
CROPPED_PATH = "F:\\Media\\"
QR_PATH = "special://skin/media/QR/charm/"

CROP_X = 208
CROP_Y = 85
CROP_W = 400
CROP_H = 130

def get_latest_screenshot():
    files = os.listdir(MEDIA_PATH)
    bmp_files = [f for f in files if re.match(r"screenshot\d{3}\.bmp", f.lower())]
    if not bmp_files:
        return None
    bmp_files.sort()
    return os.path.join(MEDIA_PATH, bmp_files[-1])

def wait_for_file_ready(filepath, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(filepath, 'rb'):
                return True
        except IOError:
            xbmc.sleep(500)
    return False

def crop_bmp_region(input_path, output_path, x, y, w, h):
    with open(input_path, 'rb') as f:
        header = f.read(54)
        magic, size, reserved1, reserved2, offset = struct.unpack('<2sIHHI', header[:14])
        if magic != b'BM':
            raise ValueError("Not a BMP file")

        width, height, planes, bpp, compression = struct.unpack('<iiHHI', header[18:34])
        if bpp != 24 or compression != 0:
            raise ValueError("Only 24-bit uncompressed BMP supported")

        row_size = ((bpp * width + 31) // 32) * 4
        new_row_size = ((24 * w + 31) // 32) * 4
        cropped_data = []

        f.seek(offset)
        top_bmp_row = height - 1 - y
        bottom_bmp_row = height - y - h

        for row_index in range(height):
            row = f.read(row_size)
            if bottom_bmp_row <= row_index <= top_bmp_row:
                start = x * 3
                end = (x + w) * 3
                cropped_row = row[start:end]
                padding = b'\x00' * (new_row_size - len(cropped_row))
                cropped_data.append(cropped_row + padding)

        new_size = 54 + new_row_size * h
        new_header = bytearray(header)
        struct.pack_into('<I', new_header, 2, new_size)
        struct.pack_into('<i', new_header, 18, w)
        struct.pack_into('<i', new_header, 22, h)
        struct.pack_into('<I', new_header, 34, new_row_size * h)

        with open(output_path, 'wb') as out:
            out.write(new_header)
            for row in cropped_data:
                out.write(row)

def encode_multipart_formdata(fields, files):
    boundary = uuid.uuid4().hex
    crlf = b'\r\n'
    lines = []

    for key, value in fields.items():
        lines.append(b'--' + boundary.encode('ascii'))
        disposition = 'Content-Disposition: form-data; name="{}"'.format(key)
        lines.append(disposition.encode('utf-8'))
        lines.append(b'')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif not isinstance(value, bytes):
            value = str(value).encode('utf-8')
        lines.append(value)

    for key, filename, value in files:
        lines.append(b'--' + boundary.encode('ascii'))
        disposition = 'Content-Disposition: form-data; name="{}"; filename="{}"'.format(key, filename)
        lines.append(disposition.encode('utf-8'))
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.append(('Content-Type: {}'.format(content_type)).encode('utf-8'))
        lines.append(b'')
        lines.append(value)

    lines.append(b'--' + boundary.encode('ascii') + b'--')
    lines.append(b'')

    body = crlf.join(lines)
    content_type = 'multipart/form-data; boundary={}'.format(boundary)
    return content_type, body


def upload_to_catbox(filepath):
    url = 'https://litterbox.catbox.moe/resources/internals/api.php'

    with open(filepath, 'rb') as f:
        file_data = f.read()

    fields = {'reqtype': 'fileupload', 'time': '24h'}
    files = [('fileToUpload', os.path.basename(filepath), file_data)]

    content_type, body = encode_multipart_formdata(fields, files)

    req = urllib2.Request(url, data=body)
    req.add_header('Content-Type', content_type)
    req.add_header('Content-Length', str(len(body)))

    try:
        resp = urllib2.urlopen(req)
        response_text = resp.read()
        if isinstance(response_text, bytes):
            response_text = response_text.decode('utf-8')
        return response_text
    except Exception as e:
        return None

def download_qr_code(url, save_path):
    qr_api_url = "https://api.qrcode-monkey.com/qr/custom"
    qr_data = {
        "data": url,
        "config": {
            "body": "square",
            "eye": "frame0",
            "eyeBall": "ball0",
            "gradientColor1": "#d27cae",
            "gradientColor2": "#a04d7a",
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

        with open(save_path, "wb") as f:
            f.write(response.read())

        return True

    except Exception as e:
        xbmcgui.Dialog().ok("Error", "Failed to download QR code:\n" + str(e))
        return False


def show_image_with_slideshow(image_path):
    slideshow_dir = QR_PATH
    if not os.path.exists(slideshow_dir):
        os.makedirs(slideshow_dir)

    temp_image_path = os.path.join(slideshow_dir, "qr_preview.png")
    shutil.copy(image_path, temp_image_path)

    xbmc.executebuiltin('SlideShow("{}",notrandom)'.format(slideshow_dir))


def main():
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.sleep(2500)
    xbmc.executebuiltin('TakeScreenshot()')
    xbmc.sleep(1000)

    latest = get_latest_screenshot()
    if not latest or not wait_for_file_ready(latest):
        xbmcgui.Dialog().ok("Error", "Screenshot file not ready")
        return

    username = xbmc.getInfoLabel('System.ProfileName').strip()
    if not username:
        username = 'user'

    cropped_path = os.path.join(CROPPED_PATH, "cortanaCharm-{}.bmp".format(username))

    try:
        crop_bmp_region(latest, cropped_path, CROP_X, CROP_Y, CROP_W, CROP_H)
        xbmcgui.Dialog().ok("Cropped", "Saved: " + cropped_path)

        # Ask user if they want to upload (uses litterbox.catbox.moe for 24 hour temporary storage)
        yes_no = xbmcgui.Dialog().yesno("cortanaCharm", "Upload cropped image to catbox.moe for 24 hours?")
        if not yes_no:
            xbmcgui.Dialog().ok("Cancelled", "Upload cancelled by user.")
            return

        url = upload_to_catbox(cropped_path)
        if url:
            xbmcgui.Dialog().ok("cortanaCharm - Upload Complete", url)

            # Ask if user wants to preview QR code
            if xbmcgui.Dialog().yesno("View QR Code", "Show QR code for uploaded URL?"):
                qr_path = os.path.join(QR_PATH, "cortanaCharm.png")
                if download_qr_code(url, qr_path):
                    show_image_with_slideshow(qr_path)
                    xbmc.executebuiltin('Skin.SetBool(cortanaCharmScreenshot)')
                else:
                    xbmcgui.Dialog().ok("QR Error", "Could not generate QR code.")
        else:
            xbmcgui.Dialog().ok("Upload Failed", "Could not upload the file.")
    except Exception as e:
        xbmcgui.Dialog().ok("Error", str(e))

main()
