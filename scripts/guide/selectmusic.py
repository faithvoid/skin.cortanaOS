# This is incredibly hacky, but works well enough. Needs more formats.

import xbmc
import xbmcgui
import os

default_path = ""  # Set a default media folder
dialog = xbmcgui.Dialog()

supported_exts = ('.mp3', '.wav', '.flac', '.cdda', '.mp4', '.avi', '.mkv', '.mov',
                  '.wmv', '.mpeg', '.mpg', '.wma', '.3gp', '.strm', '.m3u', '.m3u8')

file_path = dialog.browse(1, "Select a Media File", "files", "|".join(supported_exts), False, False, default_path)

if file_path:
    folder_path = os.path.dirname(file_path)
    selected_file = os.path.basename(file_path)

    all_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(supported_exts)
    ])

    try:
        selected_index = all_files.index(selected_file)
    except ValueError:
        xbmc.executebuiltin('Notification(Error,File not found in folder,5000)')
        raise SystemExit

    ext = os.path.splitext(selected_file)[1].lower()
    playlist_type = xbmc.PLAYLIST_MUSIC if ext in ('.mp3', '.wav', '.flac', '.cdda', '.wma', '.m3u', '.m3u8', '.strm') else xbmc.PLAYLIST_VIDEO

    playlist = xbmc.PlayList(playlist_type)
    playlist.clear()

    reordered_files = all_files[selected_index:] + all_files[:selected_index]

    for file in reordered_files:
        full_path = os.path.join(folder_path, file)
        label = file
        list_item = xbmcgui.ListItem(label)
        playlist.add(full_path, list_item)

    xbmc.Player().play(playlist)
