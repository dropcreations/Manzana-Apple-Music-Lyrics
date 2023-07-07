# __Manzana Apple Music Lyrics__

A python program to fetch lyrics from apple music albums and songs and then generates lyrics videos from fetched time-synced lyrics. See [here](#manzana-pro)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/manzana__dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/manzana__light.png">
  <img alt="Apple Music" src="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/manzana__light.png">
</picture>

## __How to use?__

First of all clone this project or download the project as a zip file and extract it to your pc or see [releases](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics/releases).

```
git clone https://github.com/dropcreations/Manzana-Apple-Music-Lyrics.git && cd Manzana-Apple-Music-Lyrics
```

Install required modules for python (use `pip3` if `pip` doesn't work for you)

```
pip install -r requirements.txt
```

Get your Apple Music cookies from web browser and search for `media-user-token` and get it.

|Domain|Include subdomains|Path|Secure|Expiry|Name|Value
|---|---|---|---|---|---|---|
|.apple.com|TRUE|/|FALSE|0|geo|##|
|.apple.com|TRUE|/|TRUE|0|dslang|##-##|
|.apple.com|TRUE|/|TRUE|0|site|###|
|.apple.com|TRUE|/|TRUE|0|myacinfo|#####...|
|.music.apple.com|TRUE|/|TRUE|1680758167|commerce-authorization-token|#####...|
|.apple.com|TRUE|/|FALSE|1715317057|itspod|##|
|.music.apple.com|TRUE|/|TRUE|1681361859|media-user-token|#####...|
|.music.apple.com|TRUE|/|TRUE|1681361859|itre|#|
|.music.apple.com|TRUE|/|TRUE|1681361859|pldfltcid|#####...|
|.music.apple.com|TRUE|/|TRUE|1681361859|pltvcid|#####...|
|.music.apple.com|TRUE|/|TRUE|1681361859|itua|##|

Paste `media-user-token` when it asked for...

open terminal and run below command (Use `py` or `python3` if `python` doesn't work for you)

```
python manzana.py [album or song url]
```

When saving time synced lyrics, timestamps are in `00:00.00` format. If you want to get it in `00:00.000` format use `--sync` or `-s` as below

```
python manzana.py -s [album or song url]
```

Get help using `-h` or `--help` command

```
usage: manzana.py [-h] [-v] [-s] [--no-txt] [--no-lrc] url

Manzana: Apple Music Lyrics

positional arguments:
  url            Apple Music URL for an album or a song

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -s, --sync     Save timecode's in 00:00.000 format (three ms points)
  --no-txt       Don't save lyrics as a .txt file
  --no-lrc       Don't save time-synced lyrics as a .lrc file
```

## Manzana Pro

You can create lyric videos using __Apple Music__, if you have an user subscription. What you just need to do is get `Manzana Pro` program and extract it to a specified folder using the installer and add that folder to your system `PATH` variable. Make sure you have `ffmpeg` also in your `PATH`. You can also customize background image of the output video and frame-rate (FPS).

```
usage: manzana [-h] [-v] [-b BACKGROUND] [-f FPS] url

Manzana: Apple Music Lyric Videos

positional arguments:
  url                   Apple Music URL for an album or a song.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -b BACKGROUND, --background BACKGROUND
                        Replace background image with your own image. Add image path.
  -f FPS, --fps FPS     Set frame-rate of the output video. (default: 24fps, max: 60fps)
```

Progress preview of [__Ava Max - Hold Up (Wait a Minute)__](https://music.apple.com/lk/album/hold-up-wait-a-minute/1634875613?i=1634875618)

![progress_preview](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/console_preview.gif)

- See output [here](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/preview_pro.mp4)

![output_preview](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/output_preview.gif)

### How to get Manzana Pro?

- You can get `Manzana Pro` for just __$19__.
- Contact me via `dropcodestudio@gmail.com` for further infomation.

## Manzana Premium

___COMING SOON...___

![output_preview](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/output_preview_premium.gif)

- See output [here](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/preview_premium.mp4)

## About me

Hi, I'm Dinitha. You might recognize me as GitHub's [dropcreations](https://github.com/dropcreations).

__Other useful python scripts done by me__

| Project              | Github location                                              |
|----------------------|--------------------------------------------------------------|
| Apple-Music-Tagger   | https://github.com/dropcreations/Manzana-Apple-Music-Tagger  |
| MKVExtractor         | https://github.com/dropcreations/MKVExtractor                |
| FLAC-Tagger          | https://github.com/dropcreations/FLAC-Tagger                 |
| MP4/M4A-Tagger       | https://github.com/dropcreations/MP4-Tagger                  |
| MKV-Tagger           | https://github.com/dropcreations/MKV-Tagger                  |

<br>

- __NOTE: If you found any issue using this script mention in issues section__
