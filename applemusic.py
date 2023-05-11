import os
import re
import json
import requests
from loggings import Logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

logger = Logger("AppleMusic")

class AppleMusic(object):
    def __init__(self, syncPoints: int):
        self.session = requests.Session()
        self.session.headers = {
            'content-type': 'application/json;charset=utf-8',
            'connection': 'keep-alive',
            'accept': 'application/json',
            'origin': 'https://music.apple.com',
            'referer': 'https://music.apple.com/',
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        self.sync_points = int(syncPoints)
        self.__get_access_token()
        self.__load_cookies()

    def __check_url(self, url):
        try:
            urlopen(url)
            return True
        except (URLError, HTTPError):
            return False
        
    def __get_url(self, url):
        parsed_url = urlparse(url)

        if not parsed_url.scheme:
            url = "https://" + url # Add a default scheme if none is present

        if parsed_url.netloc == "music.apple.com":
            if self.__check_url(url):
                splits = url.split('/')

                __id = splits[-1]
                __kind = splits[4]

                if __kind == "album":
                    if len(__id.split('?i=')) > 1:
                        __id = __id.split('?i=')[1]
                        __kind = "song"

                self.kind = __kind
                self.id = __id
            else: logger.error("URL is invalid!", 1)
        else: logger.error("URL is invalid!", 1)
        
    def __get_access_token(self):
        logger.info("Fetching access-token...")

        response = requests.get('https://music.apple.com/us/browse')
        if response.status_code != 200: raise Exception(response.text)

        index_js = re.search('(?<=index)(.*?)(?=\.js")', response.text).group(1)
        response = requests.get(f'https://music.apple.com/assets/index{index_js}.js')
        if response.status_code != 200: raise Exception(response.text)

        access_token = re.search('(?=eyJh)(.*?)(?=")', response.text).group(1)
        
        self.session.headers.update({
            'authorization': f'Bearer {access_token}'
        })

    def __media_user_token(self, cookies):
        if "media-user-token" in cookies:
            logger.info("Fetching media-user-token...")

            self.session.headers.update({
                "media-user-token": cookies.get("media-user-token")
            })

            response = self.session.get("https://amp-api.music.apple.com/v1/me/storefront")
            response = json.loads(response.text)

            user_storefront = response["data"][0].get("id")
            user_language = response["data"][0]["attributes"].get("defaultLanguageTag")

            self.storefront = user_storefront
            self.language = user_language

            self.session.headers.update({
                'accept-language': f'{self.language},en;q=0.9'
            })

    def __get_cookies_txt(self, cookie_file):
        cookies = {}
        with open(cookie_file, 'r') as c:
            for line in c:
                if not re.match(r'^\#', line):
                    items = line.strip().split("\t")
                    if len(items) > 1: cookies[items[5]] = items[6]
        return cookies

    def __get_cookies_json(self, cookie_file):
        cookies = {}
        with open(cookie_file, 'r') as c:
            c_json = json.load(c)
            for item in c_json:
                cookies[item.get("name")] = item.get("value")
        return cookies

    def __load_cookies(self):
        self.cookies_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies")

        logger.info("Loading cookies...")
        if not os.path.exists(self.cookies_dir):
            os.makedirs(self.cookies_dir)
            logger.error("Cookies not found! paste cookies into ./config/cookies", 1)
        else:
            cookie_files = os.listdir(self.cookies_dir)
            if len(cookie_files) != 0:
                for cookie_file in cookie_files:
                    cookie_file = os.path.join(self.cookies_dir, cookie_file)

                    if os.path.splitext(cookie_file)[1] == ".txt":
                        cookies = self.__get_cookies_txt(cookie_file)
                    elif os.path.splitext(cookie_file)[1] == ".json":
                        cookies = self.__get_cookies_json(cookie_file)

                self.__media_user_token(cookies)
            else:
                logger.error("Cookies not found! paste cookies into ./config/cookies", 1)

    def __get_json(self):
        logger.info("Getting API response...")
        apiUrl = f'https://amp-api.music.apple.com/v1/catalog/{self.storefront}/{self.kind}s/{self.id}'

        self.session.params = {
            'include[songs]': 'albums,lyrics',
            'l': f'{self.language}'
        }

        response = self.session.get(apiUrl)
        return json.loads(response.text)
    
    def __get_ts(self, ts):
        ts = ts.replace('s', '')
        secs = float(ts.split(':')[-1])

        if ":" in ts: mins = ts.split(':')[-2]
        else: mins = 0

        if self.sync_points == 3: return f'{mins:0>2}:{secs:06.3f}'
        elif self.sync_points == 2: return f'{mins:0>2}:{secs:05.2f}'
    
    def __get_lyrics(self, _ttml):
        ttml = BeautifulSoup(_ttml, "lxml")

        _normalLyrics = []
        _syncedLyrics = []

        if not 'itunes:timing="None"' in _ttml:
            for line in ttml.find_all("p"):
                if "span" in str(line):
                    span = BeautifulSoup(str(line), "lxml")
                    for s in span.find_all("span", attrs={'begin': True, 'end': True}):
                        begin = self.__get_ts(s.get("begin"))
                        _syncedLyrics.append(f"[{begin}]{s.text}")
                else:
                    begin = self.__get_ts(line.get("begin"))
                    _syncedLyrics.append(f"[{begin}]{line.text}")

        for line in ttml.find_all("p"):
            _normalLyrics.append(line.text)

        return {
            "lyrics": _normalLyrics,
            "timeSyncedLyrics": _syncedLyrics
        }
    
    def __get_errors(self, errors):
        if not isinstance(errors, list): errors = [errors]
        for error in errors:
            err_status = error.get("status")
            err_detail = error.get("detail")
            logger.error(f"{err_status} - {err_detail}", 1)
    
    def __get_album(self):
        data = self.__get_json()
        
        if not "errors" in data:
            logger.info("Fetching album info...")

            lyrics = []

            attributes = data["data"][0].get("attributes")
            relationships = data["data"][0].get("relationships")

            for track in relationships["tracks"].get("data"):
                __tracks = {
                    "album": attributes.get("name"),
                    "albumArtist": attributes.get("artistName"),
                    "trackNumber": track["attributes"].get("trackNumber"),
                    "track": track["attributes"].get("name"),
                    "trackArtist": track["attributes"].get("artistName")
                }

                if "lyrics" in track["relationships"]:
                    if len(track["relationships"]["lyrics"].get("data")) > 0:
                        __tracks.update(self.__get_lyrics(track["relationships"]["lyrics"]["data"][0]["attributes"].get("ttml")))

                lyrics.append(__tracks)

            return lyrics
        else:
            self.__get_errors(data.get("errors"))

    def __get_song(self):
        data = self.__get_json()

        if not "errors" in data:
            logger.info("Fetching song info...")

            lyrics = []

            attributes = data["data"][0]["relationships"]["albums"]["data"][0].get("attributes")
            for track in data.get("data"):
                __tracks = {
                    "album": attributes.get("name"),
                    "albumArtist": attributes.get("artistName"),
                    "trackNumber": track["attributes"].get("trackNumber"),
                    "track": track["attributes"].get("name"),
                    "trackArtist": track["attributes"].get("artistName")
                }

                if "lyrics" in track["relationships"]:
                    if len(track["relationships"]["lyrics"].get("data")) > 0:
                        __tracks.update(self.__get_lyrics(track["relationships"]["lyrics"]["data"][0]["attributes"].get("ttml")))

                lyrics.append(__tracks)

            return lyrics
        else:
            self.__get_errors(data.get("errors"))
    
    def get_info(self, url):
        self.__get_url(url)
        if self.kind == "album": return self.__get_album()
        elif self.kind == "song": return self.__get_song()
        else: logger.error("Only albums and songs are supported!", 1)
