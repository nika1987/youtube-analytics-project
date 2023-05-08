import os

from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

from helper.youtube_api_manual import youtube

load_dotenv(find_dotenv())
api_key: str = os.getenv('YT_API_KEY')





class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

vdud = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")

print(vdud.print_info())
