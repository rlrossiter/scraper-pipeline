import abc

import bs4


class SoupProcessorBase(abc.ABC):
    """
    Class for processing a parsed HTML page
    """

    @abc.abstractclassmethod
    def process(self, soup: bs4.BeautifulSoup) -> str:
        """
        Process the parsed HTML. Returns a string.
        """
        raise NotImplementedError
