from typing import Union
from utils import create_directory, get_json_attribute
from models import TweetModel

import requests
import os


def get_tweet_model(tweet: dict) -> TweetModel:
    # Get Media URLs
    media_urls: list[str] = []

    extended_entities: dict = tweet.get("extended_entities")
    if extended_entities == None:
        # The tweet does not contain any extended entities,
        # and therefore has no media
        return None

    all_media: list[dict] = extended_entities.get("media")
    if all_media == None:
        # The tweet does not contain any media
        return None

    for media in all_media:
        if media.get("type") != get_json_attribute("options", "media_type"):
            continue
        media_url: str = media.get("media_url")
        media_url_https: str = media.get("media_url_https")

        # Prioritize https over http when possible
        if media_url_https is not None:
            media_urls.append(media_url_https)
        elif media_url is not None:
            media_urls.append(media_url)

    # If no get_json_attribute("options", "media_type") exist
    if len(media_urls) == 0:
        return None

    # Get other data
    tweet_id = tweet.get("id")
    created_at = tweet.get("created_at")

    user: dict = tweet.get("user")
    user_id = user.get("id")
    user_name = user.get("name")
    user_screen_name = user.get("screen_name")

    return TweetModel(
        tweet_id, created_at, media_urls, user_id, user_name, user_screen_name
    )


def get_all_tweet_model(tweets: list[dict]) -> list[TweetModel]:
    tweet_models: list[TweetModel] = []
    for tweet in tweets:
        tweet_model = get_tweet_model(tweet)
        if tweet_model is not None:
            tweet_models.append(get_tweet_model(tweet))
    return tweet_models


def download_tweet(tweet: Union[TweetModel, dict]):
    directory_path = get_json_attribute("options", "folder_name")
    create_directory(directory_path)

    if type(tweet) == dict:
        tweet_model: TweetModel = get_tweet_model(tweet)
        if get_tweet_model is None:
            media_type = get_json_attribute("options", "media_type")
            print(f'No media of type "{media_type}" was found.')
            return
    elif type(tweet) == TweetModel:
        tweet_model: TweetModel = tweet

    for media_url in tweet_model.media_urls:
        image_format = get_json_attribute("options", "image_format")
        image_size = get_json_attribute("options", "image_size")
        modified_media_url = f"{media_url}?format={image_format}&name={image_size}"

        image = requests.get(modified_media_url)

        # TODO: Add customizable file names based on TweetModel
        file_name = f"{tweet_model.user_screen_name} - {tweet_model.tweet_id}_{image_size}.{image_format}"
        file_path = os.path.join(directory_path, file_name)

        with open(file_path, "wb") as f:
            f.write(image.content)


def download_all_tweets(tweets: list[dict]) -> None:
    directory_path = get_json_attribute("options", "folder_name")
    create_directory(directory_path)

    tweet_models = get_all_tweet_model(tweets)
    if tweet_models is None:
        media_type = get_json_attribute("options", "media_type")
        print(f'No media of type "{media_type}" was found.')
        return

    for tweet_model in tweet_models:
        download_tweet(tweet_model)
