from config import path
from api import BSDownloader
import argparse

from colorama import Fore

s = BSDownloader()

def print_multiple(lines) -> None:
    for l in lines:
        print(l)

def print_title() -> None:
    print_multiple([
        f"============================================================",
        f"BeatSaber Map Downloader by github.com/novialriptide",
        f" [!] do ctrl+c to exit program",
        f"============================================================",
    ])

def print_map_success(hash: str) -> None:
    """Success Message"""
    map_name = s.get_map_by_hash(hash)["name"]
    print(f"{Fore.LIGHTGREEN_EX}Downloaded: {map_name}{Fore.RESET}")

def print_map_fail(hash: str) -> None:
    """Fail Message"""
    print(f"{Fore.LIGHTRED_EX}Failed to download: {hash}{Fore.RESET}\nMake sure you copy and pasted the hash correctly.\nCreate an issue here: https://github.com/novialriptide/BeatSaber-Installer/issues")

print_title()

while(True):
    hash = input(" > ")
    try:
        s.download_map_by_hash(path, hash)
        print_map_success(hash)
    except Exception as e:
        print_map_fail(hash)
        print(e)