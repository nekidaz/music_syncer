import time
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict, Optional

from clients.music_client import MusicClient
from models.track import Track
from mappers.spotify_mapper import SpotifyTrackMapper  # добавлен маппер

from models.track import Tracks


class SpotifyClient(MusicClient):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8080/callback"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.sp: Optional[spotipy.Spotify] = None
        self.logger = logging.getLogger(__name__)

        self.scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
        self.auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=self.scope,
            cache_path=".spotify_cache"
        )

        self._authenticate()

    def _authenticate(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager, language="ru")
            user = self.sp.current_user()
            self.logger.info(f"Подключен к Spotify как: {user['display_name']} ({user['id']})")
        except Exception as e:
            self.logger.error(f"Ошибка аутентификации Spotify: {e}")
            raise

    def get_current_user(self) -> Dict:
        try:
            return self.sp.current_user()
        except Exception as e:
            self.logger.error(f"Ошибка получения пользователя: {e}")
            raise

    def get_or_create_playlist(self, name: str) -> str:
        try:
            user_id = self.sp.current_user()["id"]
            playlists = self.sp.current_user_playlists(limit=50)
            for playlist in playlists["items"]:
                if playlist["name"].lower() == name.lower():
                    return playlist["id"]
            created = self.sp.user_playlist_create(user=user_id, name=name, public=False)
            return created["id"]
        except Exception as e:
            self.logger.error(f"Ошибка при поиске/создании плейлиста '{name}': {e}")
            raise

    def get_liked_tracks(self, limit: int = 50, offset: int = 0) -> List[Track]:
        try:
            results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
            return [SpotifyTrackMapper.from_raw(item) for item in results["items"]]
        except Exception as e:
            self.logger.error(f"Ошибка получения лайкнутых треков: {e}")
            raise

    def get_all_liked_tracks(self) -> Tracks:
        try:
            all_tracks = Tracks()
            offset = 0
            limit = 50

            while True:
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset, market="RU")
                items = results.get("items", [])
                if not items:
                    break



                mapped_tracks = [SpotifyTrackMapper.from_raw(item) for item in items]
                all_tracks.extend(mapped_tracks)

                offset += limit
                time.sleep(0.2)

            return all_tracks
        except Exception as e:
            self.logger.error(f"Ошибка получения всех любимых треков: {e}")
            raise
