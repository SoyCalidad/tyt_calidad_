from abc import ABC
from html.parser import HTMLParser


class HTMLFilter(HTMLParser, ABC):
    """
    A simple no deps HTML -> TEXT converter.
    @see https://stackoverflow.com/a/55825140
    """
    text = ''

    def handle_data(self, data):
        self.text += data
        
