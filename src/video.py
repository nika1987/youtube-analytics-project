import os
import json
import datetime
import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        """
        Инициализация класса Video
        """
        self.video_id = video_id
        response = self.youtube.videos().list(part="snippet,statistics", id=self.video_id).execute()
        #print(response)
        self.title = response["items"][0]["snippet"]["title"]
        self.url = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.views = response["items"][0]["statistics"]["viewCount"]
        self.likes = response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.title


class PLVideo(Video):
    """ Инициализация наследоваемого класса PLVideo """
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):

        """
        Инициализация класса PlayList

        """
        self.playlist_id = playlist_id
        self._response = self.youtube.playlists().list(part="snippet", id=self.playlist_id).execute()
        #print(self._response)
        self.title_list = self._response["items"][0]["snippet"]["title"]
        self.url_list = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает общую длительность плейлиста.
        Returns:
            timedelta: Общая длительность плейлиста.
        """
        video_id = []
        for item in self._response["items"]:
            print(item)
            video_id.append(item["contentDetails"]["videoId"])

        response = self.youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(video_id)
                                                     ).execute()
        duration = datetime.timedelta()
        for item in response["items"]:
            duration += isodate.parse_duration(item["contentDetails"]["duration"])
        return duration

