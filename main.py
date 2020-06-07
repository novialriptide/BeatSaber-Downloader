from colorama import Fore
from colorama import Style
from colorama import Back
from beatdownloader_api import *
from EDIT_ME import *
import json
import threading
import os

TITLE_MSG = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}BeatSaber Custom Level Installer{Fore.RESET}{Back.RESET}",
    f"Developed by u/NovialRiptide"
])

COMMANDS = [
    "I", # download beatmap by ID
    "M", # download multiple beatmaps
]

INVALID_COMMAND_ERROR_MSG = combine_multiple_lines([
    f"{Fore.WHITE}{Back.RED}Error: Invalid Command{Fore.RESET}{Back.RESET}",
    f"Please try again."
])

COMMAND1_MSG0 = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}Input your search setting{Fore.RESET}{Back.RESET}",
    f"{Fore.GREEN}1{Fore.RESET} Trending",
    f"{Fore.GREEN}2{Fore.RESET} Date Ranked",
    f"{Fore.GREEN}3{Fore.RESET} Scores Set",
    f"{Fore.GREEN}4{Fore.RESET} Star Rating",
    f"{Fore.GREEN}5{Fore.RESET} Author"
])

COMMAND1_MSG1 = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}Input the download limit{Fore.RESET}{Back.RESET}"
])

COMMAND1_MSG2 = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}Ranked? (y/n){Fore.RESET}{Back.RESET}"
])

l = os.listdir(path)
song_database = []
for folder_name in l:
    song_database.append(folder_name.split(' ')[0])

threads = []
print(TITLE_MSG)
while(True):
    command_input = input("> ")
    if command_input == COMMANDS[0]:
        beatsaver_id = input("Input BeatSaver ID to install\n> ")
        data = get_beatsaver_data(beatsaver_id)
        print_beatsaver_data(data)
        thread = threading.Thread(target=download_beatmap, args=[path, beatsaver_id, song_database])
        threads.append(thread)
        thread.start()
        thread.join()
        print("Finished!")
        threads.remove(thread)
        
    elif command_input == COMMANDS[1]:
        setting_search = input(f"{COMMAND1_MSG0}\n> ")
        limit = input(f"{COMMAND1_MSG1}\n> ")
        ranked = input(f"{COMMAND1_MSG2}\n> ")
        if ranked == "y": ranked = 1
        if ranked == "n": ranked = 0
        data = get_scoresaber_data(int(setting_search)-1, int(limit))
        songs_downloaded = 1
        songs_to_download = len(data["songs"])
        for song in data["songs"]:
            if song["ranked"] == ranked:
                print_scoresaber_data(song)
                print(f"Processing... ({songs_downloaded}/{songs_to_download})")
                thread = threading.Thread(target=download_beatmap, args=[path, song["id"], song_database])
                threads.append(thread)
                thread.start()
                thread.join()
                threads.remove(thread)
                songs_downloaded += 1

    else:
        print(INVALID_COMMAND_ERROR_MSG)