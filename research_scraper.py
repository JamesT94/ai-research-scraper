"""
Main script that pulls in all the other scrapers
"""

import gartner_scraper
import forrester_scraper
import idc_scraper

search_terms = ['ai', 'artificial intelligence', 'machine learning', 'big data']

idc_scraper.get_csv(search_terms)
forrester_scraper.get_csv(search_terms)
gartner_scraper.get_csv(search_terms)
