# This is incredibly hacky, but works well enough. Needs more formats.

import xbmc
import xbmcgui
import xbmcaddon
import os
import json

# Set the default directory for browsing
default_path = ""  # Optionally set a default folder
dialog = xbmcgui.Dialog()

# Define supported extensions
audio_exts = {'.mp3', '.wav', '.flac', '.cdda', '.wma', '.m3u', '.m3u8', '.strm'}
video_exts = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.mpeg', '.mpg', '.3gp', '.m3u', '.m3u8', '.strm'}
mask = "|".join(audio_exts | video_exts)  # Combine extensions for dialog

# Open file selection dialog
file_path = dialog.browse(1, "Select a Media File", "files", mask, False, False, default_path)

if file_path:
    ext = os.path.splitext(file_path)[1].lower()
    base_file = os.path.basename(file_path)

    if ext in audio_exts or ext in video_exts:
        playlist_type = "audio" if ext in audio_exts else "video"

        json_cmd = {
            "jsonrpc": "2.0",
            "method": "Playlist.Add",
            "params": {
                "playlistid": 0 if playlist_type == "audio" else 1,  # 0=Music, 1=Video
                "item": {"file": file_path}
            },
            "id": 1
        }

        xbmc.executeJSONRPC(json.dumps(json_cmd))

        # Show confirmation
        xbmc.executebuiltin(f'Notification(Added to Queue,{base_file},3000)')
    else:
        xbmc.executebuiltin('Notification(Error, Unsupported file type, 5000)')
