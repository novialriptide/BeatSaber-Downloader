from colorama import Fore
from colorama import Style
from colorama import Back
from beatdownloader_api import *
from EDIT_ME import *
import json
import os
import argparse
import threading

TITLE_MSG = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}BeatSaber Custom Level Installer{Fore.RESET}{Back.RESET}",
    f"Developed by u/NovialRiptide"
])

def DOWNLOAD_SUMMARY_MSG(downloaded, ignored, passed, limit):
    lines = [
        f"{Fore.BLACK}{Back.WHITE}Download Summary{Fore.RESET}{Back.RESET}",
        f"{Fore.GREEN}Songs Downloaded{Fore.RESET} {downloaded}",
        f"{Fore.GREEN}Songs Ignored{Fore.RESET} {ignored}",
        f"{Fore.GREEN}Songs Passed{Fore.RESET} {passed}",
        f"{Fore.GREEN}Download Limit{Fore.RESET} {limit}"
    ]
    border_line = get_border_line(lines)
    lines.insert(0,border_line)
    return combine_multiple_lines(lines)

l = os.listdir(path)
song_database = []
for folder_name in l:
    song_database.append(folder_name.split(' ')[0])

parser = argparse.ArgumentParser()
parser.add_argument("--id")
parser.add_argument("--multiple")

args = parser.parse_args()
if args.id:
    try:
        beatsaver_id = args.id
        data = get_beatsaver_data(beatsaver_id)
        print_beatsaver_data(data)
        download_beatmap(path, beatsaver_id, song_database)
        print("Finished!")
    except json.decoder.JSONDecodeError:
        print("Unknown ID")

elif args.multiple:
    setting_search = args.multiple
    ss_data = get_scoresaber_data(int(setting_search)-1, int(DOWNLOAD_LIMIT))

    songs_passed = 0
    songs_download = 0
    songs_ignored = 0
    songs_to_download = len(ss_data["songs"])

    for song in ss_data["songs"]:
        bs_data = get_beatsaver_data(song["id"])
        songs_passed += 1
        try:
            star_range_test = STAR_RANGE[0] <= int(song["stars"]) <= STAR_RANGE[1]
            rank_test = song["ranked"] == RANKED
            key_test = bs_data["key"] not in song_database
            if rank_test and star_range_test and key_test:
                songs_download += 1
                print_scoresaber_data(song)
                thread = threading.Thread(target=download_beatmap, args=[path, song["id"], song_database])
                download_beatmap(path, song["id"], song_database)
            elif key_test == False:
                songs_ignored += 1
                print_scoresaber_data(song)
                print("This song is already downloaded.")
        except:
            songs_ignored += 1
            print_scoresaber_data(song)
            print("This song is ignored due to an unexpected error.")
            
        print(f"song {Fore.GREEN}#{songs_passed}{Fore.RESET} passed. ({Fore.GREEN}{songs_to_download-songs_passed}{Fore.RESET} left)")
    print("\n" + DOWNLOAD_SUMMARY_MSG(songs_download,songs_ignored,songs_passed, songs_to_download))

    songs_passed = 0
    songs_download = 0
    songs_ignored = 0
    songs_to_download = 0

else:
    print(TITLE_MSG)