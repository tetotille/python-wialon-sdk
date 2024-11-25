import dotenv
import os

from datetime import datetime
from wialon import Wialon


dotenv.load_dotenv("../.env")
url = os.getenv("WIALON_URL")
api_key = os.getenv("API_KEY")

wialon = Wialon(url,api_key)

items = wialon.items.search(by="property",item_type="unit")

for item in items["items"]:
    print("-----------------------------------")
    print(item["nm"].upper())
    messages = wialon.messages.load_interval(item["id"],datetime(2024,10,1),datetime(2024,11,20))
    print(messages)
    print("-----------------------------------")    