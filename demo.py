from scraper_pipeline.fanout import bestbuy_sku_to_url_fanout
from scraper_pipeline.models import scrape
from scraper_pipeline.models import subscriber
from scraper_pipeline.notify import notifier
from scraper_pipeline.process import state_processor
from scraper_pipeline.scrape.plugin import best_buy_processor
from scraper_pipeline.scrape import scraper

skus = ["6419920", "6428324"]

subscribers = [
    subscriber.Subscriber(page_id="6419920", address="Ryan", wait_seconds=300)
]

def notify_callable(page_id, old, new, addr, meta):
    print("NOTIFYING")
    print(f"Product: {page_id}")
    print(f"State: {new}")
    print(f"Address: {addr}")
    print(f"Metadata: {meta}")

fanout = bestbuy_sku_to_url_fanout.BestBuySkuFanout(skus)
to_scrape = fanout.fanout()

bby_proc = best_buy_processor.BestBuyProcessor()
scraper_obj = scraper.Scraper()

for s in to_scrape:
    state = scraper_obj.scrape(s, bby_proc)
    print(f"Page content: {state}")

    state_proc = state_processor.StateProcessor()
    notification = state_proc.process(state)

    if notification:
        print(f"Notification: {notification}")
        notifier_obj = notifier.Notifier(notify_callable)
        notifier_obj.notify_change(notification, [], subscribers)