from sqlmodel import Field, SQLModel

class Song(SQLModel, table = True):
    name: str = Field(primary_key=True)
    artist: str
    duration_seconds: int = Field(gt=0)
    genre: str | None


class Playlist(SQLModel, table = True):
    name: str = Field(primary_key=True)

class SongInPlaylist(SQLModel, table=True):
    song: str = Field(primary_key=True, foreign_key="song.name")
    playlist: str = Field(primary_key=True, foreign_key="playlist.name")



if __name__ == "__main__":
    song1 = Song(name="Yellow submarine", artist="The beatles", duration_seconds=180, genre="Classic")
    print(song1)