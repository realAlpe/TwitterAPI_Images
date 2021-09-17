from api import *
import logging


def configurations():
    # Setting up logger
    logging.basicConfig(
        filename="log_data.log",
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )


if __name__ == "__main__":
    configurations()

    schedule_download_home_timeline()
    # download_tweet_by_id(1438278046423867392)

# Future ideas:

# what about just creating another script that sorts the image files based on their prefix (username) in the file
# and the API thingy just puts all images into one folders where you can check all the images
# once you delete all of the ones that you dont want to have in your collection
# you can execute the script and it will sort everything automatically

# maybe fix the issue with retweets (and get their media)

# make it so that no duplicate images can be created (possible issues with retweets)
