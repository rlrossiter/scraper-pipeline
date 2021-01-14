import typing

from scraper_pipeline.models import scrape


class BestBuySkuFanout(object):
    def __init__(self, skus: typing.List[str]):
        self._skus = skus
        self._url_format = "https://api.bestbuy.com/click/-/%s/pdp"

    def fanout(self) -> typing.List[scrape.Scrape]:
        return [
            scrape.Scrape(
                page_id=sku,
                url=self._url_format % sku
            )
            for sku in self._skus
        ]
