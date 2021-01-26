# AI Research Web Scraper

## Overview
The purpose of this tool is to scrape recently published reports from the research and advisory companies, Gartner, Forrester, and IDC. There are several customisable elements of the main script that are detailed below in the '[How To Use](#how-to-use)' section.

The main script [research_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/research_scraper.py) utilises the following customised web scraping scripts.  

- [gartner_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/gartner_scraper.py)
- [forrester_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/forrester_scraper.py)
- [idc_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/idc_scraper.py)

## How To Use
The [research_scraper.py](https://github.com/JamesT94/ai-research-scraper/blob/main/research_scraper.py) script can be executed from the command line and then you'll be asked for the following inputs.  


`---SCRAPING OPTIONS---`  
`The scraping options available are: Gartner[1], Forrester[2], IDC[3], All[4]`  
`Please select an option (1-4): `  

`---SEARCH TERMS---`  
`The current search terms are: `  
`['ai', 'artificial intelligence', 'machine learning', 'big data']`  
`Press Enter to continue`

`---OUTPUT DIRECTORY---`  
`The output files will be saved in the following directory: `  
`D:\GithubRepos\ai-research-scraper`  
`Press 1 to continue or 2 to change the directory:`  

`---FINAL CONFIRMATION---`  
`Scraping: Gartner`  
`Search Terms: ['ai', 'artificial intelligence', 'machine learning', 'big data']`  
`Output Directory: D:\GithubRepos\ai-research-scraper`  

`Press Enter to begin...`


## Progress Monitoring
I've used tqdm to add a simplisitc progress bar to each stage of the process.

![Progress Bar](https://github.com/JamesT94/ai-research-scraper/blob/main/imgs/progress_bar.png)

After collating a full list of all pages to visit the scraper will remove any duplicates before visiting each page and saving the required data.

## Outputs
The program will output a single .csv file containing all outputs.
