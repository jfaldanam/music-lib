import os
from argparse import ArgumentParser

from sqlmodel import Session, SQLModel, create_engine, select

db_engine = None

db_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:my-secret-pw@localhost:3306/")

db_debug_flag = bool(os.getenv("DEBUG", False))


def init_db():
    """Database initialization function."""
    global db_engine
    db_engine = create_engine(db_url, echo=db_debug_flag)
    SQLModel.metadata.create_all(db_engine)

def execute_command(arguments):
    # our application logic
    if arguments.create_playlist is not None:
        print("Creating playlist. Playlist name=", arguments.create_playlist)
    elif arguments.add_song is not None:
        print("Adding song to playlist.", arguments.add_song)
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
    execute_command(arguments)