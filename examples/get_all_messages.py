"""This script gets all messages from all units in the account."""

# pyright: basic
import os
from datetime import datetime

from dotenv import load_dotenv

from wialon import Wialon

load_dotenv("../.env")
url = os.getenv("WIALON_URL")
api_key = os.getenv("API_KEY")

if url is None or api_key is None:
    msg = "Missing URL or API key"
    raise ValueError(msg)

wialon = Wialon(url, api_key)

items = wialon.items.search(by="property", item_type="unit")

# ruff: noqa
for item in items:
    print("-----------------------------------")
    print(item["nm"].upper())
    messages = wialon.messages.load_interval(
        item["id"],
        datetime(2024, 10, 1),
        datetime(2024, 11, 20),
    )
    print(messages)
    print("-----------------------------------")
# ruff: enable
