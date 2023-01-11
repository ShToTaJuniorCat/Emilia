from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from json import loads

# Literally everything possible to do with spotipy!
scope = "ugc-image-upload " \
        "user-modify-playback-state " \
        "user-read-playback-state " \
        "user-read-currently-playing " \
        "user-follow-modify " \
        "user-follow-read " \
        "user-read-recently-played " \
        "user-read-playback-position " \
        "user-top-read " \
        "playlist-read-collaborative " \
        "playlist-modify-public " \
        "playlist-read-private " \
        "playlist-modify-private " \
        "app-remote-control " \
        "streaming " \
        "user-read-email " \
        "user-read-private " \
        "user-library-modify " \
        "user-library-read"

with open("credentials.json", "r") as handle:
    credentials = loads(handle.read())

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, client_id=credentials['client_id'], client_secret=credentials['client_secret'], redirect_uri=credentials['redirect_uri'])
)


def get_time(args):
    return f"Now is {datetime.now().strftime('%H:%M:%S')}"

def search(args):
    pass


def start_app(args):
    pass


def is_playing():
    return sp.currently_playing()['is_playing']


def play_pause_music(args):
    if is_playing():
        state = "paused"
        sp.pause_playback()
    else:
        state = "playing"
        sp.start_playback()

    return f"Music is now {state}."


def next_track(args):
    sp.next_track()
    return "Sure."


def previous_track(args):
    sp.previous_track()
    return "Sure."


def get_uri(name, search_type):
    return sp.search(name, 1, type=search_type)[search_type + "s"]["items"][0]["uri"]


def play_track_by_name(args):
    sp.start_playback(uris=[get_uri(args.lower(), "track")])
    return "Enjoy!"


def queue_track_by_name(args):
    sp.add_to_queue(uri=get_uri(args.lower(), "track"))
    return "Enjoy!"


def toggle_shuffle(args):
    sp.shuffle(args == "on")
    return f"Shuffle is now {args == 'on'}."


def command_to_function(command):
    translator = {
        "time": get_time,
        "search": search,
        "open": start_app,
        "pause": play_pause_music,
        "resume": play_pause_music,
        "next": next_track,
        "previous": previous_track,
        "play": play_track_by_name,
        "shuffle": toggle_shuffle,
        "queue": queue_track_by_name
    }

    try:
        return translator[command]
    except KeyError:
        return lambda args: "Unknown command."


inp = input("> ")

while inp != "exit":
    inp = inp.split(" ")
    cmd = inp[0]
    args = None

    if len(inp) > 1:
        args = " ".join(inp[1:])

    print(command_to_function(cmd)(args))

    inp = input("> ")
