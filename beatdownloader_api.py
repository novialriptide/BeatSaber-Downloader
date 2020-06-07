from colorama import Fore
from colorama import Style
from colorama import Back
import requests
import urllib
import json
import zipfile
import os

header = {
    "User-Agent": "CumDumpster/6.66"
}

opener = urllib.request.build_opener()
opener.addheaders = [("User-Agent", "CumDumpster/6.66")]
urllib.request.install_opener(opener)

def get_scoresaber_data(cat_option,limit):
    """
    0 = trending
    1 = date ranked
    2 = scores set
    3 = star rating
    4 = author
    """
    if 0 <= cat_option <= 4:
        r = requests.get(f"http://scoresaber.com/api.php?function=get-leaderboards&cat={cat_option}&page=1&limit={limit}")
        return r.json()
    else:
        raise Exception("cat_option is out of range")

def get_beatsaver_data(id):
    r = requests.get(f"https://beatsaver.com/api/maps/by-hash/{id}", headers=header)
    return r.json()

def get_difficulties(data):
    data = data["metadata"]["difficulties"]
    difficulty_keys = list(data.keys())
    valid_difficulties = []
    valid_difficulties_display = []
    for key in range(len(difficulty_keys)):
        if data[difficulty_keys[key]]:
            valid_difficulties.append(difficulty_keys[key])
            
            displayString = difficulty_keys[key].capitalize()
            displayString = displayString.replace("plus", "+")
            valid_difficulties_display.append(displayString)

    return valid_difficulties, valid_difficulties_display

def download_beatmap(path, id):
    def clean_text(text):
        valid_chars = [' ','-','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
        new_text = ''
        for char in text:
            if char.lower() in valid_chars:
                new_text += char
        return new_text
    r = requests.get(f"https://beatsaver.com/api/maps/by-hash/{id}", headers=header)
    data = r.json()
    song_author = clean_text(f"{data['metadata']['songName']} - {data['metadata']['songAuthorName']}")
    download_url = f"https://beatsaver.com{data['directDownload']}"

    urllib.request.urlretrieve(download_url, f"temp{id}.zip")
    extract_path = f"{path}\{data['key']} ({song_author})"
    with zipfile.ZipFile(f"temp{id}.zip","r") as zip_ref:
        zip_ref.extractall(path=extract_path)
    os.remove(f"temp{id}.zip")

def combine_multiple_lines(lines):
    value = ""
    for line in lines:
        value = value + line + "\n"
    return value

def get_border_line(lines):
    count = 0
    for line in lines:
        if len(line) > count:
            count = len(line)

    border_line = ""
    for x in range(count):
        border_line = border_line + "="

    return border_line

def print_beatsaver_data(data):
    meta_data = data["metadata"]
    stats = data["stats"]
    duration = list(str(meta_data['duration']/60))
    duration = duration[0] + duration[1] + duration[2]
    lines = [
        f"{meta_data['songAuthorName']} - {meta_data['songName']}",
        "",
        f"{Fore.GREEN}ID{Fore.RESET} {data['_id']}",
        f"{Fore.GREEN}Level Author{Fore.RESET} {meta_data['levelAuthorName']}",
        f"{Fore.GREEN}Difficulties{Fore.RESET} {get_difficulties(data)[1]}",
        f"{Fore.GREEN}Duration{Fore.RESET} {duration} minute(s)",
        f"{Fore.GREEN}Rating{Fore.RESET} {stats['upVotes']}/{stats['downVotes']}",
        f"{Fore.GREEN}BPM{Fore.RESET} {meta_data['bpm']}"
    ]
    border_line = get_border_line(lines)
    lines.insert(0,border_line)
    print(combine_multiple_lines(lines))