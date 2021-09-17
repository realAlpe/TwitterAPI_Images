from time import sleep
from tweet_functions import download_all_tweets, download_tweet
from tweepy import OAuthHandler, API, Status
from logging import getLogger
from os import environ
from utils import (
    get_options_attribute,
    get_since_id,
    open_directory,
    set_json,
    set_since_id,
)

import schedule


LOGGER = getLogger()


def get_api() -> API:
    # Authenticate and get the API
    API_KEY = environ["TWITTER_API_KEY"]
    API_KEY_SECRET = environ["TWITTER_API_KEY_SECRET"]
    ACCESS_TOKEN = environ["TWITTER_ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = environ["TWITTER_ACCESS_TOKEN_SECRET"]

    auth = OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return API(auth)


def download_home_timeline() -> None:
    LOGGER.info("Started downloading home timeline.")

    api = get_api()

    # Define constants
    COUNT = 1000
    since_id = get_since_id()

    # Retrieve all tweets since the last tweet
    status_tweets: list[Status] = api.home_timeline(
        since_id=since_id, count=COUNT, exclude_replies="true"
    )

    # Return early if no tweets exist
    if len(status_tweets) == 0:
        LOGGER.info("No new tweets were found.")
        return

    # Sort out and download all tweets with media
    tweets: list[dict] = list(map(lambda x: x._json, status_tweets))
    download_all_tweets(tweets)

    # Update the since_id in order to avoid duplication
    set_since_id(tweets[0].get("id"))

    if get_options_attribute("open_directory_on_closing"):
        open_directory()

    LOGGER.info("Finished downloading home timeline.")


def schedule_download_home_timeline() -> None:
    download_home_timeline()
    minutes_count = get_options_attribute("repeat_every_x_minutes")
    schedule.every(minutes_count).minutes.do(download_home_timeline)
    while True:
        schedule.run_pending()
        sleep(5)


def download_tweet_by_id(id: int) -> None:
    api = get_api()
    json_data = api.get_status(id)._json
    download_tweet(json_data)


def debug(id: int) -> None:
    api = get_api()
    json_data = api.get_status(id)._json
    set_json("debug", json_data)
