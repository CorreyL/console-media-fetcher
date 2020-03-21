import tweepy
import yaml

with open("tokens.yaml") as tokens:
    tokens = yaml.load(tokens, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(tokens["api_key"], tokens["api_secret_key"])
auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])

api = tweepy.API(auth)
