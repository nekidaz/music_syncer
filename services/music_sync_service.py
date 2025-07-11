from clients import SpotifyClient, YoutubeMusicClient
from models.track import Track
import logging

class MusicSyncService:
    def __init__(self, youtube_music_client: YoutubeMusicClient, spotify_client: SpotifyClient):
        self.youtube_music_client = youtube_music_client
        self.spotify_client = spotify_client
        self.logger = logging.getLogger(__name__)

    def sync_liked_songs_to_youtube_music(self, ytm_playlist_name: str = "Spotify Liked Songs"):

        self.logger.info("Загружаем любимые треки из Spotify...")
        liked_tracks: list[Track] = list(self.spotify_client.get_all_liked_tracks())
        self.logger.info(f"Найдено {len(liked_tracks)} любимых треков")

        # 2. Получаем или создаем плейлист в YouTube Music
        playlist_id = self.youtube_music_client.get_or_create_playlist(ytm_playlist_name)

        # 3. Получаем текущие треки из YouTube Music плейлиста
        existing_tracks = self.youtube_music_client.get_playlist_tracks(playlist_id)
        self.logger.info(f"В плейлисте YouTube Music сейчас {len(existing_tracks)} треков")

        # 4. Вычисляем новые треки для добавления
        tracks_to_add = [
            track for track in liked_tracks
            if not self.youtube_music_client.track_exists_in_list(track, existing_tracks)
        ]

        # 5. Вычисляем лишние треки для удаления
        tracks_to_remove = [
            track for track in existing_tracks
            if not self.youtube_music_client.track_exists_in_list(track, liked_tracks)
        ]

        self.logger.info(f"{len(tracks_to_add)} новых треков для добавления")
        self.logger.info(f"{len(tracks_to_remove)} треков будет удалено")


        for track in tracks_to_add:
            self.youtube_music_client.search_and_add_to_playlist(track, playlist_id)

        # 7. Удаляем лишние треки
        for track in tracks_to_remove:
            self.youtube_music_client.remove_track_from_playlist(track, playlist_id)

        self.logger.info("Синхронизация завершена.")

