# AI Research Web Scraper

## Overview
The purpose of this tool is to scrape recently published reports from the research and advisory companies, Gartner, Forrester, and IDC. There are several customisable elements of the main script that are detailed below in the '[How To Use](#how-to-use)' section.

The main script [research_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/research_scraper.py) utilises the following customised web scraping scripts.  

- [gartner_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/gartner_scraper.py)
- [forrester_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/forrester_scraper.py)
- [idc_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/idc_scraper.py)

## How To Use
The [research_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/research_scraper.py) script can be executed from the command line and then you'll be asked for the following inputs.  


1. The sites available for scraping are: Gartner`[1]`, Forrester`[2]`, IDC`[3]`, All`[4]`
Please select an option (1-4).

2. The current search terms are: `[AI, Artificial Intelligence, Machine Learning, etc.]`
Please Enter to continue.

3. The output files will be saved in the following directory:
Press Enter to continue or type 1 to change the directory.

4. Scraping: All
Search Terms: `[AI, Artificial Intelligence, Machine Learning, etc.]`
Output Directory: ...

The entire scraping process may take up to 30 minutes for all sites.
Press Enter to begin...
