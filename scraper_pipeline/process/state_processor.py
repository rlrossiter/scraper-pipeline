from scraper_pipeline.models import page_content
from scraper_pipeline.models import state_change_notification


class StateProcessor(object):
    """
    Processes the state of a scraped page
    """

    def process(
        self,
        state: page_content.PageContent
    ) -> state_change_notification.StateChangeNotification:
        """
        Process a page to see if there are any state changes.

        If there is no state change, the returned StateChangeNotification is None
        """

        # Cheating for now as we will assume the previous page state is 'Sold Out'
        # We could pay attention to previous page state at page_id
        # and create a notification if the state is different from previous page state
        notification = None
        if (state.content is not None and state.content != 'Sold Out'):
            md = {'url': state.url}
            notification = state_change_notification.StateChangeNotification(
                page_id=state.page_id,
                old_state='Sold Out',
                new_state=state.content,
                metadata=md
            )

        return notification
