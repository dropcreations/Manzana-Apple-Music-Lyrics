import os
import argparse
from loggings import Logger
from applemusic import AppleMusic
from sanitize_filename import sanitize

logger = Logger("Downloader")

LOGO = """


                 ███╗   ███╗ █████╗ ███╗   ██╗███████╗ █████╗ ███╗   ██╗ █████╗ 
                 ████╗ ████║██╔══██╗████╗  ██║╚══███╔╝██╔══██╗████╗  ██║██╔══██╗
                 ██╔████╔██║███████║██╔██╗ ██║  ███╔╝ ███████║██╔██╗ ██║███████║
                 ██║╚██╔╝██║██╔══██║██║╚██╗██║ ███╔╝  ██╔══██║██║╚██╗██║██╔══██║
                 ██║ ╚═╝ ██║██║  ██║██║ ╚████║███████╗██║  ██║██║ ╚████║██║  ██║
                 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                   ──── Apple Music Lyrics ────                 


"""

downloads = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
if not os.path.exists(downloads): os.makedirs(downloads)

def main():
    parser = argparse.ArgumentParser(
        description="Manzana: Apple Music lyrics downloader"
    )
    parser.add_argument(
        '-sp',
        '--sync-points',
        choices=[2, 3],
        default=3,
        help="Miliseconds point count in synced lyrics",
    )
    parser.add_argument(
        'url',
        help="url from Apple Music for a album, song or music-video",
        type=str
    )
    args = parser.parse_args()

    applemusic = AppleMusic(syncPoints=args.sync_points)
    data = applemusic.get_info(args.url)

    for lyrics in data:
        album = lyrics.get("album")
        album_artist = lyrics.get("albumArtist")
        track_no = str(lyrics.get("trackNumber")).zfill(2)
        track_name = lyrics.get("track")
        track_artist = lyrics.get("trackArtist")

        album_dir = os.path.join(downloads, sanitize(f"{album_artist} - {album}"))
        txt_file = os.path.join(album_dir, sanitize(f"{track_no} - {track_artist} - {track_name}.txt"))
        txt__log = f"{track_no} - {track_name}.txt"
        lrc_file = os.path.join(album_dir, sanitize(f"{track_no} - {track_artist} - {track_name}.lrc"))
        lrc__log = f"{track_no} - {track_name}.lrc"

        if not os.path.exists(album_dir):
            os.makedirs(album_dir)

        if "lyrics" in lyrics:
            if len(lyrics.get("lyrics")) > 0:
                logger.info(f'Saving "{txt__log}"...')
                with open(txt_file, "w", encoding="utf-8") as txt:
                    txt.write("\n".join(lyrics.get("lyrics")))
            else: logger.warning(f"No lyrics for {txt__log}")
        else: logger.warning(f"No lyrics for {txt__log}")

        if "timeSyncedLyrics" in lyrics:
            if len(lyrics.get("timeSyncedLyrics")) > 0:
                logger.info(f'Saving "{lrc__log}"...')
                with open(lrc_file, "w", encoding="utf-8") as lrc:
                    lrc.write("\n".join(lyrics.get("timeSyncedLyrics")))
            else: logger.warning(f"No lyrics for {lrc__log}")
        else: logger.warning(f"No lyrics for {lrc__log}")

    logger.info("Successfully completed.")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(LOGO)
    main()