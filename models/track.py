from dataclasses import dataclass

@dataclass
class Track:
    name: str
    artist: str
    album: str

    def normalize(self, text: str) -> str:
        return text.lower().strip()

    def is_equal(self, other: 'Track') -> bool:
        return (
            self.normalize(self.name) == self.normalize(other.name) and
            self.normalize(self.artist) == self.normalize(other.artist)
        )


class Tracks:
    def __init__(self, tracks: list[Track] = None) -> None:
        self.tracks = tracks or []

    def track_exists(self, track: Track) -> bool:
        return any(t.is_equal(track) for t in self.tracks)

    def add(self, track: Track) -> None:
        self.tracks.append(track)

    def extend(self, tracks: list[Track]) -> None:
        self.tracks.extend(tracks)

    def __len__(self):
        return len(self.tracks)

    def __iter__(self):
        return iter(self.tracks)
