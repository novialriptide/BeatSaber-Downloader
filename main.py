from colorama import Fore
from colorama import Style
from colorama import Back
from beatdownloader_api import *
import json
import threading
import os

path = "C:\Program Files (x86)\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels"
#path = r"C:\Users\novia\Desktop"

TITLE_MSG = combine_multiple_lines([
    f"{Fore.BLACK}{Back.WHITE}BeatSaber Custom Level Installer{Fore.RESET}{Back.RESET}",
    f"Developed by u/NovialRiptide"
])

COMMANDS = [
    "I", # download beatmap by ID
    "M"  # download multiple beatmaps
]

threads = []
while(True):
    print(TITLE_MSG)
    
    #command_input = input("> ")
    command_input = "I"
    if command_input == COMMANDS[0]:    
        beatsaver_id = input("Input BeatSaver ID to install\n> ")
        data = get_beatsaver_data(beatsaver_id)
        print_beatsaver_data(data)
        thread = threading.Thread(target=download_beatmap, args=[path, beatsaver_id])
        threads.append(thread)
        thread.start()
        thread.join()
        print("Finished!")
        threads.remove(thread)