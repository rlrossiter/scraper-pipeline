from scraper_pipeline.scrape import soup_processor_base


class BestBuyProcessor(soup_processor_base.SoupProcessorBase):
    def process(self, soup):
        return soup.find_all(class_='add-to-cart-button')[0].text
