import os
import sys

from sanitize_filename import sanitize

from api import AppleMusic
from utils import logger

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

CACHE = os.path.join(__get_path(), "cache")
CONFIG = os.path.join(__get_path(), "config")

def __sanitize(path):
    if path != "":
        return sanitize(path)
    return path

def arguments(args):
    if args.no_lrc and args.no_txt:
        logger.warning(
            "Nothing to save! Don't use '--no-lrc' and '--no-txt' at same time..."
        )
    else:
        syncMsPointCount = 2
        if args.sync: syncMsPointCount = 3

        applemusic = AppleMusic(CACHE, CONFIG, syncMsPointCount)
        data = applemusic.getInfo(args.url)

        __dir = data.get("dir")
        if not os.path.exists(__dir):
            os.makedirs(__sanitize(__dir))

        for track in data["tracks"]:
            __file = track.get("file")

            if not args.no_lrc:
                path = os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.lrc")
                if os.path.exists(path):
                    logger.warning(f'"{__file}.lrc" is already exists!')
                else:
                    if "timeSyncedLyrics" in track:
                        if track.get("timeSyncedLyrics"):
                            logger.info(f'Saving "{__file}.lrc"...')
                            with open(path, "w", encoding="utf-8") as l:
                                l.write(
                                    '\n'.join(
                                        track.get("timeSyncedLyrics")
                                    )
                                )
                        else: logger.warning(f'No time-synced lyrics for "{__file}"')
                    else: logger.warning(f'No time-synced lyrics for "{__file}"')

            if not args.no_txt:
                path = os.path.join(__sanitize(__dir), f"{__sanitize(__file)}.txt")
                if os.path.exists(path):
                    logger.warning(f'"{__file}.txt" is already exists!')
                else:
                    if "lyrics" in track:
                        if track.get("lyrics"):
                            logger.info(f'Saving "{__file}.txt"...')
                            with open(path, "w", encoding="utf-8") as l:
                                l.write(
                                    '\n'.join(
                                        track.get("lyrics")
                                    )
                                )
                        else: logger.warning(f'No lyrics for "{__file}"')
                    else: logger.warning(f'No lyrics for "{__file}"')

    logger.info("Done.")
