import logging
import random
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from collections import namedtuple
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import pandas as pd 


Album = namedtuple('Album', 'album_title image_url')


def get_next_url(path: str = 'urls.csv', threshold: int = 120) -> str:
    """Get a random url that hasn't been tweeted in at least {threshold} runs.
    
    Args:
        path (str): path pointing to a csv containing urls
        threshold (int): number of runs to consider when filtering recently tweeted urls
        
    Returns:
        str: url for an album on Apple Music
    """
    df = pd.read_csv(path)
    potential = df[df['runs_since_used'] >= threshold] # filter those below the threshold
    i = random.randrange(0, len(potential)) # generate random index
    url = potential.iat[i, 0]

    # increment runs counter for all urls by 1, set chosen to zero
    df['runs_since_used'] = df['runs_since_used'].apply(lambda x: x + 1)
    j = df['url'].loc[lambda x: x == url].index[0] # find corresponding index in original df
    df.iat[j, 1] = 0 
    df.to_csv(path, index=False)

    return url


def scrape_apple_music(album_url: str) -> Album:
    """Scrape Apple Music album page to extract the 
    artist/album title and album cover image url.

    Args:
        album_url (str): url of specific album page on Apple Music, i.e.,
                         'https://music.apple.com/ca/album/thriller/269572838'

    Returns:
        Album: namedtuple containing album title and image url
    """
    try:
        html = requests.get(album_url).text
        soup = BeautifulSoup(html, 'html.parser')
        album = soup.find("meta", property="og:title")
        if album is not None:
            album_title = album['content']
            image_url = str(soup.find('source')).split(f'srcset="')[1].split(' 500w')[0]
            logging.info(f"{album_title}, {image_url} returned from Apple Music")
            return Album(album_title, image_url)
        else:
            logging.warning(f"Data for {album_url} not found")
    except ConnectionError:
        logging.warning(f"{album_url} not found, connection failed")


def get_image(image_url: str) -> Image.Image:
    """Get image from specified URL and resize.
    Once in a while, Apple Music simply won't let us grab an image from a specified link
    In that case, we have to skip that album and move on to the next

    Args:
        image_url (str): url of image to fetch

    Returns:
        Image.Image: resized image object for prediction
    """
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).resize((224, 224))
        return img
    except UnidentifiedImageError:
        logging.warning(f"{image_url} not found, record skipped and deleted")
