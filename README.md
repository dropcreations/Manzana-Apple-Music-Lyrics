# __Manzana-Apple-Music-Lyrics__

A python script to fetch lyrics from apple music albums and songs.

<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/logo-in-dark.png">
<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/logo-in-light.png">
<img alt="Apple Music" src="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-Music-Lyrics/main/assets/logo-in-light.png">
</picture>

## __How to use?__

First of all clone this project or download the project as a zip file and extract it to your pc.

```
git clone https://github.com/dropcreations/Manzana-Apple-Music-Lyrics.git && cd Manzana-Apple-Music-Lyrics
```

Install required modules for python (use `pip3` if `pip` doesn't work for you)

```
pip install -r requirements.txt
```

Get your Apple Music cookies from web browser and paste it in `./cookies` folder.<br>
Doesn't matter if cookies in `.txt` or `.json` format, both are accepted.

open terminal and run below command (Use `py` or `python3` if `python` doesn't work for you)

```
python manzana.py [album or song url]
```

When saving time synced lyrics, timestamps are in `00:00.000` format. If you want to get it in `00:00.00` format set `--sync-points` as `2` as below

```
python manzana.py --sync-points 2 [album or song url]
```

Get help using `-h` or `--help` command

```
usage: manzana.py [-h] [-sp {2,3}] url

Manzana: Apple Music lyrics downloader

positional arguments:
  url                                URL from Apple Music for a album, song or music-video

optional arguments:
  -h, --help                         Show this help message and exit
  -sp {2,3}, --sync-points {2,3}     Miliseconds point count in synced lyrics
```

## About me

Hi, I'm Dinitha. You might recognize me as GitHub's [dropcreations](https://github.com/dropcreations).

__Other usefull python scripts done by me__

| Project              | Github location                                              |
|----------------------|--------------------------------------------------------------|
| Apple-Music-Tagger   | https://github.com/dropcreations/Manzana-Apple-Music-Tagger  |
| MKVExtractor         | https://github.com/dropcreations/MKVExtractor                |
| FLAC-Tagger          | https://github.com/dropcreations/FLAC-Tagger                 |
| MP4/M4A-Tagger       | https://github.com/dropcreations/MP4-Tagger                  |
| MKV-Tagger           | https://github.com/dropcreations/MKV-Tagger                  |

<br>

- __NOTE: If you found any issue using this script mention in issues section__
