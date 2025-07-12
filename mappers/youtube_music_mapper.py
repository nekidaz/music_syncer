from models.track import Track

class YTMusicTrackMapper:
    @staticmethod
    def from_raw(data: dict) -> Track:
        return Track(
            name=data.get("title", "Unknown Title"),
            artist=data["artists"][0]["name"] if data.get("artists") else "Unknown Artist",
            album=data["album"]["name"] if data.get("album") else "Unknown Album"
        )
