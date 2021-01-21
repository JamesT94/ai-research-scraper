"""
Main script that pulls in all the other scrapers
"""

import pandas as pd
import gartner_scraper
import forrester_scraper
import idc_scraper

search_terms = ['ai', 'artificial intelligence', 'machine learning', 'big data']

gartner_df = gartner_scraper.get_csv(search_terms)
forrester_df = forrester_scraper.get_csv(search_terms)
idc_df = idc_scraper.get_csv(search_terms)


full_df = pd.concat([forrester_df, idc_df, gartner_df])
full_df.to_csv('research.csv', encoding='utf-8-sig', index=False)
