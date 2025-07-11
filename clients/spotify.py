import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict, Optional, Generator
import logging
from models.track import Track

class SpotifyClient:

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
        """Аутентификация в Spotify"""
        try:
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

            # Проверяем подключение
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


    def get_liked_tracks(self, limit: int = 50, offset: int = 0) -> List[Track]:
        try:
            results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
            tracks = []
            for item in results['items']:
                track_data = item['track']
                track = Track(
                    name=track_data['name'],
                    artist=track_data['artists'][0]['name'],
                    album=track_data['album']['name']
                )
                tracks.append(track)
            return tracks

        except Exception as e:
            self.logger.error(f"Ошибка получения лайкнутых треков: {e}")
            raise

    def get_all_liked_tracks(self) -> list[Track]:
        try:
            all_tracks = []
            offset = 0
            limit = 50

            while True:
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                items = results.get('items', [])
                if not items:
                    break

                for item in items:
                    track_data = item['track']
                    track = Track(
                        name=track_data['name'],
                        artist=track_data['artists'][0]['name'],
                        album=track_data['album']['name']
                    )
                    all_tracks.append(track)

                offset += limit
                time.sleep(0.2)

            return all_tracks

        except Exception as e:
            self.logger.error(f"Ошибка получения всех любимых треков: {e}")
            raise



