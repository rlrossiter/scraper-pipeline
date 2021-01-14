import requests
import time

import bs4

from scraper_pipeline.scrape import soup_processor_base
from scraper_pipeline.models import page_content
from scraper_pipeline.models import scrape

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"


class Scraper(object):
    """
    Class used for scraping a web page
    """

    def __init__(self):
        self._headers = {'User-Agent': USER_AGENT}

    def scrape(
        self,
        to_scrape: scrape.Scrape,
        processor: soup_processor_base.SoupProcessorBase
    ) -> page_content.PageContent:
        """
        Scrapes a web page and returns the state of the page
        """

        start = time.time()
        r = requests.get(to_scrape.url, headers=self._headers)
        end = time.time()
        status_code = r.status_code
        elapsed = end - start
        elapsed_ms = int(elapsed * 1000)

        if status_code == 200:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            state = processor.process(soup)
            p_state = page_content.PageContent(
                page_id=to_scrape.page_id,
                url=to_scrape.url,
                req_time=int(start),
                resp_time_ms=elapsed_ms,
                statuscode=status_code,
                content=state
            )
        else:
            p_state = page_content.PageContent(
                page_id=to_scrape.page_id,
                url=to_scrape.url,
                req_time=int(start),
                resp_time_ms=elapsed_ms,
                statuscode=status_code
            )

        return p_state
