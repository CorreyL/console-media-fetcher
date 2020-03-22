import tweepy
import yaml
import urllib.request
import os
from pytz import timezone

with open("tokens.yaml") as tokens:
    tokens = yaml.load(tokens, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(tokens["api_key"], tokens["api_secret_key"])
auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])

api = tweepy.API(auth)

public_tweets = api.home_timeline()

supported_platforms = [
    "NintendoSwitch",
    "Playstation4",
]

destination_folder_name = "media"


def main():
    media_files = []

    for tweet in public_tweets:
        # Retrieve the hashtags to know what directories to sort the downloaded
        # media in
        hashtags = tweet.entities.get("hashtags", [])
        hashtags_text = [obj["text"] for obj in hashtags]
        platform = "UnknownPlatform"
        # Iterate through the hashtags to find out what platform the media was
        # uploaded from
        for hashtag in hashtags_text:
            if hashtag in supported_platforms:
                platform = hashtag
                break
        date = tweet.created_at.astimezone()
        # Replace `:` characters with `.` to ensure the file name is usable on
        # Windows machines
        # Replace ` ` characters with `_` to make filename usage easier without
        # needing to escape the ` ` characters if ever used in a script
        reformatted_date = str(date).replace(":", ".").replace(" ", "_")
        all_media = tweet.extended_entities.get("media", [])
        if len(all_media) > 0:
            for idx, media in enumerate(all_media):
                media_url = media["media_url"]
                file_type = str(media_url).split(".")[-1]
                # The media_url will have `video` as part of the path if the file is
                # a video
                if "video" in media_url:
                    # Traverse the structure of the `extended_entities` object of
                    # the tweet to get the different processed video sizes
                    processed_videos = media.get("video_info").get("variants")
                    sorted_videos = sorted(
                        processed_videos, key=lambda obj: obj.get("bitrate", 0),
                    )
                    # TODO Make this a script argument that can be changed so that
                    # the different video qualities can be selected
                    highest_bitrate_video = sorted_videos[-1]
                    media_url = highest_bitrate_video["url"]
                    # Parse the string such as `video/mp4`
                    file_type = highest_bitrate_video["content_type"].split(
                        "/"
                    )[-1]
                media_files.append(
                    {
                        "media_url": media_url,
                        "datetime_tweeted": date,
                        "file_name": reformatted_date,
                        "file_type": file_type,
                        "platform": platform,
                        "batch_number": idx + 1,
                    }
                )

    if not os.path.exists(destination_folder_name):
        os.mkdir(destination_folder_name)

    for obj in media_files:
        media_url = obj["media_url"]
        file_name = obj["file_name"]
        file_type = obj["file_type"]
        batch_number = obj["batch_number"]
        platform = obj["platform"]
        destination = f"./{destination_folder_name}/{platform}"
        if not os.path.exists(destination):
            os.mkdir(destination)
        download = (
            f"./{destination_folder_name}/{platform}/"
            f"{file_name}_{batch_number}.{file_type}"
        )
        if not os.path.exists(download):
            urllib.request.urlretrieve(
                media_url, download,
            )


if __name__ == "__main__":
    main()
