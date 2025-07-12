from abc import ABC, abstractmethod

from models.track import Track


class MusicClient(ABC):
    @abstractmethod
    def get_all_liked_tracks(self) -> list[Track]:
        pass
    @abstractmethod
    def get_or_create_playlist(self, name: str) -> str:
        pass