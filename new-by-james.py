"""
Some info...
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
        driver.get("https://www.gartner.com/en/search?keywords=ai")  # Need to change
        # assert "Gartner" in driver.title
        pass

    def carry_out_search(self, search_term):
        driver = self.driver
        # Before searching
        search_button = driver.find_element_by_xpath("//header/section[2]/nav[1]/div[1]/div[1]/div[3]")
        search_button.click()
        search_bar = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "searchString")))
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # After searching
        # num_results = driver.find_element_by_class_name("found-result col-xs-12")  # Haven't got far enough to test
        # num_results = num_results.strip()
        # num_results = num_results.split(" ")[0]
        # print("{} results found on Gartner using search term: {}".format(num_results, search_term))
        # self.total_results[search_term] = num_results

    def scrape_save_page(self):
        driver = self.driver

        # Get all of the headings
        result_heading = driver.find_elements_by_class_name('result-heading')
        for heading in result_heading:
            print(heading.text)

        # Get all of the summaries
        result_texts = driver.find_elements_by_class_name('result-text')
        for text in result_texts:
            print(text.text)
        pass

    def next_page(self):
        pass

    def return_dataframe(self):
        pass


chromedriver_path = "C:/bin/chromedriver.exe"  # Change this to your own driver path

# Testing code
x = GartnerScraper(chromedriver_path)
x.load_webpage()
# x.carry_out_search("AI")
x.scrape_save_page()
