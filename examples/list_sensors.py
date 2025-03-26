"""This script gets all sensors from all units in the account."""

import os
import sys

from loguru import logger

from wialon import Wialon

if __name__ == "__main__":
    WIALON_URL = os.getenv("WIALON_URL")
    WIALON_TOKEN = os.getenv("WIALON_TOKEN")

    logging = logger.bind(name="sensors", rotation="500 MB")

    if not WIALON_URL or not WIALON_TOKEN:
        logging.error("Please set WIALON_URL and WIALON_TOKEN environment variables.")
        sys.exit(1)

    wialon = Wialon(WIALON_URL, WIALON_TOKEN)
    data = wialon.items.search(
        item_type="unit",
        flags=0x1 + 0x8 + 0x100 + 0x1000,
    )

    msg = f"Found {len(data)} units. {data}"
    logging.info(msg)
