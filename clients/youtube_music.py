from ytmusicapi import YTMusic, OAuthCredentials
from models.track import Track
import logging

class YoutubeMusicClient:

    def __init__(self, client_id: str, client_secret: str):
        self.logger = logging.getLogger(__name__)
        self.ytmusic = YTMusic('oauth.json', oauth_credentials=OAuthCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

    def create_playlist(self, name: str, description: str = None) -> str:
        try:
            return self.ytmusic.create_playlist(name, description or "")
        except Exception as e:
            self.logger.error(f"Ошибка при создании плейлиста: {e}")
            raise

    def get_liked_tracks(self, limit: int = 50):
        try:
            liked_tracks = []
            liked_songs = self.ytmusic.get_liked_songs(limit=limit)
            for song in liked_songs['tracks']:
                liked_tracks.append(Track(
                    name=song['title'],
                    artist=song['artists'][0]['name'],
                    album=song['album']['name'] if song.get('album') else ""
                ))
            return liked_tracks
        except Exception as e:
            self.logger.error(f"Ошибка при получении любимых треков: {e}")
            raise

    def get_or_create_playlist(self, name: str) -> str:
        try:
            playlists = self.ytmusic.get_library_playlists()
            for pl in playlists:
                if pl['title'].lower() == name.lower():
                    return pl['playlistId']
            # Если не найдено — создаём
            return self.create_playlist(name)
        except Exception as e:
            self.logger.error(f"Ошибка при поиске/создании плейлиста '{name}': {e}")
            raise

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        try:
            playlist = self.ytmusic.get_playlist(playlist_id, limit=1000)
            tracks = []
            for item in playlist['tracks']:
                tracks.append(Track(
                    name=item['title'],
                    artist=item['artists'][0]['name'],
                    album=item['album']['name'] if item.get('album') else ""
                ))
            return tracks
        except Exception as e:
            self.logger.error(f"Ошибка при получении треков из плейлиста: {e}")
            raise

    def track_exists_in_list(self, track: Track, track_list: list[Track]) -> bool:
        for t in track_list:
            if t.name.lower() == track.name.lower() and t.artist.lower() == track.artist.lower():
                return True
        return False

    def search_and_add_to_playlist(self, track: Track, playlist_id: str):
        try:
            query = f"{track.name} {track.artist}"
            results = self.ytmusic.search(query, filter="songs")
            if results:
                video_id = results[0]['videoId']
                self.ytmusic.add_playlist_items(playlist_id, [video_id])
                self.logger.info(f"Добавлен трек: {track.name} — {track.artist}")
            else:
                self.logger.warning(f"Трек не найден: {track.name} — {track.artist}")
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении трека: {track.name}: {e}")

    def remove_track_from_playlist(self, track: Track, playlist_id: str):
        try:
            playlist = self.ytmusic.get_playlist(playlist_id, limit=1000)
            tracks = playlist.get("tracks", [])
            for item in tracks:
                title = item.get("title", "").lower()
                artist = item["artists"][0]["name"].lower()
                set_video_id = item.get("setVideoId")

                if not set_video_id:
                    continue  # Без ID не удалим

                if title == track.name.lower() and artist == track.artist.lower():
                    self.ytmusic.remove_playlist_items(playlist_id, [{
                        "videoId": item["videoId"],
                        "setVideoId": set_video_id
                    }])
                    self.logger.info(f"Удалён: {track.name} — {track.artist}")
                    return

            self.logger.warning(f"Не найден для удаления: {track.name} — {track.artist}")
        except Exception as e:
            self.logger.error(f"Ошибка при удалении трека: {track.name}: {e}")
