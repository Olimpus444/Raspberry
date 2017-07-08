#!/usr/bin/env python
"""
Authors: Amr Hassan <amr.hassan@gmail.com>
         and hugovk <https://github.com/hugovk>
# Hacked from https://github.com/hugovk/bbcscrobbler
"""

import ZeroSeg.led as led
import argparse
import os
import pylast
from sys import platform as _platform
import time

API_KEY = "cff015a17177bdcedbb3a80394c9ed66"
API_SECRET = "744d6229902347830a63c8b66cbac467"

SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")

last_output = None


def output(text):
    text = str(text)
    global last_output
    if last_output == text:
        return
    else:
        last_output = text
    print(text)
    # Windows:
    if _platform == "win32":
        if "&" in text:
            text = text.replace("&", "^&")  # escape ampersand
        os.system("title " + text)
    # Linux, OS X or Cygwin:
    elif _platform in ["linux", "linux2", "darwin", "cygwin"]:
        import sys
        sys.stdout.write("\x1b]2;" + text + "\x07")


def duration(track):
    return int(track.track.get_duration())/1000


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Loopy thing to show what a Last.fm user is now playing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'user',  nargs='?', default='Olimpus444',
        help='User to check')
    args = parser.parse_args()

    network = pylast.LastFMNetwork(API_KEY, API_SECRET)

    if not os.path.exists(SESSION_KEY_FILE):
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print(
            "Please authorize the scrobbler "
            "to scrobble to your account: %s\n" % url)
        import webbrowser
        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                fp = open(SESSION_KEY_FILE, "w")
                fp.write(session_key)
                fp.close()
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = open(SESSION_KEY_FILE).read()

    network.session_key = session_key
    user = network.get_user(args.user)
    out = "Tuned in to %s" % args.user
    output(out)
    print("-" * len(out))

    playing_track = None

    while True:

        try:
            new_track = user.get_now_playing()
            # print(new_track)

            # A new, different track
            if new_track != playing_track:
                playing_track = new_track
                output(playing_track)

        except Exception as e:
            print("Error: %s" % repr(e))

        time.sleep(0.1)




device = led.sevensegment()

while True:
device.write_text(1, text)
    for _ in range(500):
	device.rotate_left()
time.sleep(0.3)


# End of file