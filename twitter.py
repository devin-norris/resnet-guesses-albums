import os
import tweepy
from dotenv import load_dotenv


def get_secrets():
    """Get API and access keys from environment"""
    load_dotenv()
    API_KEY = os.environ['API_KEY']
    API_KEY_SECRET = os.environ['API_KEY_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    return API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def twitter_authenticate() -> tweepy.api.API:
    """Authenticate to twitter APIs using tweepy"""
    API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_secrets()
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def send_tweet(payload: str, img_path: str = 'image.jpg') -> None:
    """Send tweet with payload text and temp image, then remove image"""
    api = twitter_authenticate()
    api.update_with_media(img_path, payload)
    os.remove(img_path)
    return None
