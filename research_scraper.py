"""
Main script that pulls in all the other scrapers
"""

import pandas as pd
import gartner_scraper
import forrester_scraper
import idc_scraper
import os

search_terms = ['ai', 'artificial intelligence', 'machine learning', 'big data']
scrape_option = ['Gartner', 'Forrester', 'IDC', 'All']

# Select the scraping options
print('---SCRAPING OPTIONS---')
print('The scraping options available are: Gartner[1], Forrester[2], IDC[3], All[4]')
while True:
    try:
        option_selected = int(input('Please select an option (1-4): '))
        assert(0 < option_selected < 5)
    except ValueError:
        print('You did not enter a valid option. Please try again.')
    except AssertionError:
        print('You did not enter a valid option. Please try again.')
    else:
        break

# Validate the search terms
print('\n' * 1)
print('---SEARCH TERMS---')
print('The current search terms are: ')
print(search_terms)
input('Press Enter to continue')

# Confirm or change the directory
path = os.getcwd()
print('\n' * 1)
print('---OUTPUT DIRECTORY---')
print('The output files will be saved in the following directory: ')
print(path)

while True:
    try:
        change = int(input('Press 1 to continue or 2 to change the directory: '))
        assert(0 < change < 3)
    except ValueError:
        print('You did not enter a valid option. Please try again.')
    except AssertionError:
        print('You did not enter a valid option. Please try again.')
    else:
        break

if change == 2:
    while True:
        try:
            path = input('Enter the new directory path: ')
            assert(os.path.exists(path))
        except AssertionError as error:
            print(error)
            print('File path does not exist. Please try again: ')
        else:
            break

# Pre-run checks and final confirmation
print('\n' * 2)
print('---FINAL CONFIRMATION---')
print('Scraping: ', end='')
print(scrape_option[option_selected - 1])
print('Search Terms: ', end='')
print(search_terms)
print('Output Directory: ', end='')
print(path)
print('\n' * 1)
input('Press Enter to begin scraping...')


gartner_df = gartner_scraper.get_csv(search_terms)
forrester_df = forrester_scraper.get_csv(search_terms)
idc_df = idc_scraper.get_csv(search_terms)


full_df = pd.concat([gartner_df, forrester_df, idc_df])
full_df.to_csv('research.csv', encoding='utf-8-sig', index=False)
