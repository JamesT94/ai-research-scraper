"""
Some info...
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

search_terms = ["AI", "Big Data", "Machine Learning"]  # To be looped over once we get it working


class GartnerScraper(object):
    def __init__(self, driver_path):
        self.dataframe = pd.DataFrame()
        self.driver = webdriver.Chrome(driver_path)
        self.total_results = dict()
        pass

    def load_webpage(self):
        driver = self.driver
        driver.get("https://www.gartner.com/")
        assert "Gartner" in driver.title
        pass

    def carry_out_search(self, search_term):
        driver = self.driver
        # Before searching
        search_button = driver.find_element_by_class_name("nav-icon gcom-icon-search")  # This doesn't work!
        search_button.click()
        time.sleep(5)  # Just for testing, to see if anything shows up before we start typing (sleeps for 5 seconds)
        search_bar = driver.find_element_by_id("searchString")  # Doubt this works either...
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # After searching
        num_results = driver.find_element_by_class_name("found-result col-xs-12")  # Haven't got far enough to test
        num_results = num_results.strip()
        num_results = num_results.split(" ")[0]
        print("{} results found on Gartner using search term: {}".format(num_results, search_term))
        self.total_results[search_term] = num_results

    def scrape_save_page(self):
        pass

    def next_page(self):
        pass

    def return_dataframe(self):
        pass


chromedriver_path = "C:/Users/James/Desktop/chromedriver_win32/chromedriver.exe"  # Change this to your own driver path

# Testing code
x = GartnerScraper(chromedriver_path)
x.load_webpage()
x.carry_out_search("AI")
