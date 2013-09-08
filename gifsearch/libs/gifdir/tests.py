import unittest
from .global_settings import FIREFOX_BIN_DIR
from selenium import webdriver
from gifsearch.libs.gifdir.gif_scraper import RedditParser

class ScraperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        firefox_bin = webdriver.firefox.firefox_binary.FirefoxBinary(FIREFOX_BIN_DIR)
        cls.browser = webdriver.Firefox(firefox_binary=firefox_bin)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_scraper_gif_page(self):
        self.browser.get('http://www.reddit.com/r/gif')
        self.assertIn( "Animated Gifs", self.browser.title)

    def test_scraper_check_gifs(self):
        self.browser.get('http://www.reddit.com/r/gif')
        rp = RedditParser()
        subreddit_list = rp.get_subreddit_list()
        elements = self.browser.find_elements_by_class_name('title')
        elements_list = [x for x in elements if x.tag_name == 'a']
        print [y.text for y in elements_list]
        for idx, gif_mod in enumerate(subreddit_list):
            self.assertIn(gif_mod.title, elements_list[idx].text)




if __name__ == '__main__':
    unittest.main()
