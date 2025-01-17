import os
from argparse import ArgumentParser

from model import Song, Playlist, SongInPlaylist
from sqlmodel import Session, SQLModel, create_engine, select

db_engine = None

db_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:my-secret-pw@localhost:3306/music_lib")

db_debug_flag = bool(os.getenv("DEBUG", False))


def init_db():
    """Database initialization function."""
    global db_engine
    db_engine = create_engine(db_url, echo=db_debug_flag)
    SQLModel.metadata.create_all(db_engine)

def get_song(session, name: str):
    statement = select(Song).where(Song.name == name)

    return session.exec(statement).first()


def create_song(session, name: str, artist: str, duration: str, genre: str = None):
    if get_song(session, name) is not None:
        raise ValueError("The song already exists")
    # "3:30".split(":")
    try:
        duration_int = int(duration)
    except ValueError:
        print("Error: The duration is expected in seconds as a number")
        return
    song1 = Song(name=name, artist=artist, duration_seconds=duration_int, genre=genre)
    session.add(song1)
    session.commit()

def create_playlist(session, playlist_name: str, songs: list[str]):
    
    # Check if it already exist
    playlist = Playlist(name=playlist_name)
    session.add(playlist)

    for song_name in songs:
        added_song =  SongInPlaylist(song=song_name, playlist=playlist.name)
        session.add(added_song)
    
    session.commit()

def execute_command(arguments, session):
    # our application logic
    if arguments.create_playlist is not None:
        print("Creating playlist. Playlist name=", arguments.create_playlist)

        playlist_name, *songs = arguments.create_playlist.split("|")

        # for song
            # Ensure it exists and get PK
            # if contains :
            # else PK is whatever we received

        create_playlist(session, playlist_name, songs)



    elif arguments.add_song is not None:
        print("Adding song to playlist.", arguments.add_song)
        parameters = arguments.add_song.split(":")

        if len(parameters) == 3:
            name, artist, duration = parameters
            genre = None
        elif len(parameters) == 4:
            name, artist, duration, genre = parameters
        else:
            print("Error: The application expects three or four parameters in this order: name:artist:duration(in seconds):[genre]")
            return
        create_song(session, name, artist, duration, genre)
    elif arguments.list_playlist:
        print("Listing playlists...")
    else:
        print("Unknown command, use -h for help")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--create_playlist", required=False, help="Create a playlist with a given name")
    parser.add_argument("--add_song", required=False)
    parser.add_argument("--list_playlist", required=False, action='store_true')

    arguments = parser.parse_args()
    init_db()
    with Session(db_engine) as session:
        execute_command(arguments, session)