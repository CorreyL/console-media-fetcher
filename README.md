# Console Media Fetcher

This repository contains code for a script to help users automatically download
media (i.e. videos and photos) uploaded to [Twitter](https://www.twitter.com/)
via their game consoles.

## Twitter Developer API Account

A [Twitter Developer API Account](https://developer.twitter.com/en.html) is
required to access a Twitter account's feed:

[Apply Here](https://developer.twitter.com/en/apply-for-access)

With the account, you should have 4 tokens, which needs to be placed into a
`tokens.yaml` file as follows:

```yaml
access_token: # Twitter Access Token
access_token_secret: # Twitter Access Token Secret
api_key: # Twitter API Key
api_secret_key: # Twitter API Secret Key
```

## Installation

This script was created on `Python 3.7.4`.

```bash
python -m venv venv
```

### POSIX

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows

```
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## How To Use

Once you have [downloaded all the dependencies](#Installation) and [set up your
API tokens in `tokens.yaml`](#Twitter-Developer-API-Account), run:

```
python main.py
```

And all the media files from the specified Twitter account will be downloaded.

## Formatting Code

This codebase uses [`black`](https://black.readthedocs.io/en/stable/) formatter
to ensure code consistency across the `.py` files:

```bash
black main.py -l 80
```
