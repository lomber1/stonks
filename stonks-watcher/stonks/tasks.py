import logging
from collections import Counter
from datetime import timedelta
from pprint import pprint
from typing import List

import requests
from pydantic import parse_obj_as
from stonks_types.schemas import Offer

from celeryapp import app
from config import API_URL, config
from stonks_watcher.utils import older_than


@app.task
def periodic_stonks_finder():
    # Get offers for which stonks has not been checked for more than 30 minutes (can be changed in config)
    # Only get offers which have a device
    last_stonks_check_before = older_than(timedelta(minutes=config["stonks"]["older_than"]))
    params = {
        "last_stonks_check_before": last_stonks_check_before,
        "has_device": True,
    }
    r = requests.get(f"{API_URL}/v1/offers",
                     params=params)
    offers: List[Offer] = parse_obj_as(List[Offer], r.json())
    logging.info(f"Downloaded {len(offers)} offers with outdated stonks.")

    print("------------------------------------")
    pprint(offers[5])
    print("------------------------------------")


@app.task
def find_stonks(offer: Offer):
    # Get prices for device
    device_name = offer.device.name