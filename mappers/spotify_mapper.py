from models.track import Track

class SpotifyTrackMapper:
    @staticmethod
    def from_raw(item: dict) -> Track:

        track_data = item.get("track", item)  # бывает, что приходит {"track": {...}}

        name = track_data.get("name", "Unknown Title")
        artists = track_data.get("artists", [])
        artist_name = artists[0]["name"] if artists else "Unknown Artist"
        album_name = track_data.get("album", {}).get("name", "Unknown Album")

        return Track(
            name=name,
            artist=artist_name,
            album=album_name
        )
