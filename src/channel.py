import os
import json
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
        self._channel_id = channel_id  # id канала
        self.channel = self.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        self.title: str = self.channel['items'][0]['snippet']['title']  # название канала
        self.description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.url = f"https://www.youtube.com/channel/{self._channel_id}"  # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  # количество видео
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        self._channel_id = value



    def get_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        return json.dumps(channel)

    @classmethod
    def get_service(cls):
        """Класс-метод `get_service()`, возвращающий объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """Метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра Channel"""

        data = {'channel_id': self._channel_id,
                'channel': self.channel,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriberCount': self.subscriber_count,
                'video_count': self.video_count,
                'viewCount': self.viewCount}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def __str__(self):
        return f"<{self.title}> (<{self.url}>)"

    def __add__(self, other):
        """Метод для операции сложения"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод для операции вычитания"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """Метод для операции сравнения «меньше»"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Метод для операции сравнения «меньше или равно»"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """Метод для операции сравнения «больше»"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Метод для операции сравнения «больше или равно»"""
        return int(self.subscriber_count) >= int(other.subscriber_count)

