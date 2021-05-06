import json
import logging

import requests
from scrapy import Spider
from scrapy.exceptions import CloseSpider

from stonks_scraper.items import OlxOfferItem
from stonks_types.schemas import OfferCreate


class OlxOffersPipeline:
    collection_name = "offers"
    LOG_TAG = "OlxOffersPipeline"

    def process_item(self, item: OlxOfferItem, spider: Spider):
        offer = OfferCreate(**dict(item))

        try:
            r = requests.post("http://localhost:8000/v1/offers",
                              data=offer.json(),
                              headers={'Content-type': 'application/json'})
            r.raise_for_status()

            logging.info(f"[{self.LOG_TAG}]: POSTed offer, response: code: {r.status_code}, body: {r.json()}")
        except requests.exceptions.ConnectionError:
            raise CloseSpider(f"{self.LOG_TAG}: Could not connect to API. Exiting...")

        except requests.HTTPError as e:
            raise CloseSpider(f"{self.LOG_TAG}: Creating an offer failed. Exiting...")

        return item