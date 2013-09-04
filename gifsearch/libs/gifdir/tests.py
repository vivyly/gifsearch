import unittest
from test import RedditParser

class ScraperTest(unittest.TestCase):

    def setup(self):
        self.parser = RedditParser() 

    def tearDown(self):
        pass

    def test_scraper_page_1_only(self):
        self.browser


if __name__ == '__main__':
    unittest.main( warnings='ignore' )
