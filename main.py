import tweepy
import yaml
from pytz import timezone

with open("tokens.yaml") as tokens:
    tokens = yaml.load(tokens, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(tokens["api_key"], tokens["api_secret_key"])
auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])

api = tweepy.API(auth)

public_tweets = api.home_timeline()


def main():
    media_files = []

    for tweet in public_tweets:
        date = tweet.created_at.astimezone()
        # Replace `:` characters with `.` to ensure the file name is usable on
        # Windows machines
        # Replace ` ` characters with `_` to make filename usage easier without
        # needing to escape the ` ` characters if ever used in a script
        reformatted_date = str(date).replace(":", ".").replace(" ", "_")
        media = tweet.entities.get("media", [])
        if len(media) > 0:
            media_url = media[0]["media_url"]
            file_type = str(media_url).split(".")[-1]
            media_files.append(
                {
                    "media_url": media_url,
                    "datetime_tweeted": date,
                    "file_name": reformatted_date,
                    "file_type": file_type,
                }
            )


if __name__ == "main":
    main()
