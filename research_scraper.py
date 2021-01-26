"""
Main script that pulls in all the other scrapers
"""

import pandas as pd
import gartner_scraper
import forrester_scraper
import idc_scraper
import os

search_terms = ['ai', 'artificial intelligence', 'machine learning', 'big data']
#
# gartner_df = gartner_scraper.get_csv(search_terms)
# forrester_df = forrester_scraper.get_csv(search_terms)
# idc_df = idc_scraper.get_csv(search_terms)
#
#
# full_df = pd.concat([forrester_df, idc_df, gartner_df])
# full_df.to_csv('research.csv', encoding='utf-8-sig', index=False)

# Select the scraping options
print('The scraping options available are: Gartner[1], Forrester[2], IDC[3], All[4]')
try:
    scrape_option = int(input('Please select an option (1-4): '))
    assert(scrape_option < 4)
except AssertionError as error:
    print(error)
    print('Invalid selection, please run the script again')

# Validate the search terms
print('The current search terms are: ')
print(search_terms)
input('Press Enter to continue')

# Confirm or change the directory
path = os.getcwd()
print('The output files will be saved in the following directory: ')
print(path)

change = input('Press Enter to continue or type 1 to change the directory: ')

if change == 1:
    try:
        path = input('Enter the new directory path: ')
        assert(os.path.exists(path))
    except AssertionError as error:
        print(error)
        print('File path does not exist, please run the script again')

# Pre-run checks and final confirmation
print('Scraping: ')
print(scrape_option)
print('Search Terms: ')
print(search_terms)
print('Output Directory: ')
print(path)
