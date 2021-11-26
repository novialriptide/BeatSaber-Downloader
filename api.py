from typing import List

import requests
import urllib
import zipfile
import os

class BSDownloader:
    def __init__(self):
        self.scoresaber_url = "https://scoresaber.com/api"
        self.beatsaver_url = "https://api.beatsaver.com"

    def get_leaderboard_with_filters(self, **kwargs):
        """Get a list of leaderboards based on filters

        Parameters:
            verified (bool): Filter by verified (DEPRECATION NOTICE).
            ranked (bool): Filter by ranked.
            qualified (bool): Filter by qualified.
            loved (bool): Filter by loved.
            minStar (int): Filter by minimum star value.
            maxStar (int): Filter by maximum star value.
            category (int): Category to sort by (0 = trending, date ranked = 1, scores set = 2, star difficulty = 3, author = 4).
            sort (int): Direction to sort (0 = descending, 1 = ascending).
            unique (bool): Only return one leaderboard of each id.
            page (int): Page Number.
        
        Returns:
            Leaderboard in JSON

        """
        input_url = f"{self.scoresaber_url}/leaderboards"
        valid_kwargs = ["verified", "ranked", "qualified", "loved", "minStar", "maxStar", "category", "unique", "page"]
        if kwargs is not {}:
            input_url += "?function="

        for k in kwargs:
            if k not in valid_kwargs:
                raise Exception(f"\"{k}\" is not a valid kwarg")

            input_url += f"&{k}={kwargs[k]}"

        r = requests.get(input_url)
        return r.json()

    def get_map_by_hash(self, hash: str):
        r = requests.get(f"{self.beatsaver_url}/maps/hash/{hash}")
        return r.json()

    def download_map_by_hash(
        self,
        path: str,
        hash: str
    ) -> None:
        """
        Download a map by hash via Beatsaver.com.

        Parameters:
            path: Download path.
            hash: The map's hash.

        """
        map_data = self.get_map_by_hash(hash)
        key = map_data['id']
        map_name = f"{map_data['metadata']['songName']} - {map_data['metadata']['levelAuthorName']}"
        download_url = map_data["versions"][-1]["downloadURL"] # -1 to download the latest map
        file_name = f"{key} ({map_name})"
        
        urllib.request.urlretrieve(download_url, f"{file_name}.zip")
        with zipfile.ZipFile(f"{file_name}.zip", "r") as zip:
            zip.extractall(path=f"{path}\{file_name}")
        os.remove(f"{file_name}.zip")