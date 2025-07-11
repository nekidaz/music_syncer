import time
import logging
from datetime import datetime


from clients.spotify import SpotifyClient
from clients.youtube_music import YoutubeMusicClient
from config.config import Config
from services.music_sync_service import MusicSyncService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    spotify_client = SpotifyClient(
        client_id=Config.SPOTIFY_CLIENT_ID,
        client_secret=Config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=Config.SPOTIPY_REDIRECT_URI
    )

    youtube_music_client = YoutubeMusicClient(
        client_id=Config.YOUTUBE_CLIENT_ID,
        client_secret=Config.YOUTUBE_CLIENT_SECRET
    )

    music_sync_service = MusicSyncService(youtube_music_client, spotify_client)

    logger.info("Starting music sync worker...")

    while True:
        try:
            logger.info(f"Starting sync at {datetime.now()}")

            music_sync_service.sync_liked_songs_to_youtube_music()

            logger.info("Sync completed successfully")

            logger.info("Waiting 24 hours until next sync...")
            time.sleep(86400)

        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping...")
            break
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            # При ошибке ждем 1 час перед повторной попыткой
            logger.info("Waiting 1 hour before retry...")
            time.sleep(3600)


if __name__ == "__main__":
    main()