import pytest

from scraper_pipeline.fanout import bestbuy_sku_to_url_fanout
from scraper_pipeline.models import scrape


def test_fanout():
    skus = ['1', '2', '3']
    url = ["https://api.bestbuy.com/click/-/%s/pdp" % s for s in skus]
    fanout = bestbuy_sku_to_url_fanout.BestBuySkuFanout(skus)

    scrapes = fanout.fanout()

    for s, u in zip(skus, url):
        assert scrape.Scrape(page_id=s, url=u) in scrapes