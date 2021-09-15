from datetime import datetime


class TweetModel:
    def __init__(
        self,
        tweet_id: int,
        created_at: str,
        media_urls: list[str],
        user_id: int,
        user_name: str,
        user_screen_name: str,
    ):
        self.tweet_id = tweet_id

        format = "%a %b %d %H:%M:%S %z %Y"
        self.created_at: datetime = datetime.strptime(created_at, format)

        self.media_urls = media_urls

        self.user_id = user_id
        self.user_name = user_name
        self.user_screen_name = user_screen_name
