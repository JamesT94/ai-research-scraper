"""
Need to update to search for other terms and only add the row if it doesn't already exist
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
from random import randint
from time import sleep


def create_url(url_str, page_num, search_term):
    search_term = search_term.replace(" ", "%20")
    url_str = url_str.replace('<Search_Term>', search_term)
    url_str = url_str.replace('<Page_Num>', page_num)
    return url_str


def get_soup(url):
    response = 0
    try:
        response = requests.get(url, timeout=30)
        print('Got a connection to {}'.format(url))
    except requests.exceptions.RequestException as e:
        print(e)
        try:
            response = requests.get(url, timeout=30)
            print('Got a connection to {}'.format(url))
        except requests.exceptions.RequestException as e:
            print(e)

    result_soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    return result_soup


def get_doc_list(link_list, first_search_soup, url_str, search_term):
    num_results = first_search_soup.find('div', class_='result-total').text.strip()
    num_results = num_results.split(' ')[0]
    num_pages = int(num_results) // 25

    for page in range(1, num_pages + 1):
        url = create_url(url_str, str(page), search_term)
        soup = get_soup(url)
        links = soup.find_all('a', class_='title')
        for link in links:
            link_list.append('https://www.forrester.com' + link['href'])

    return link_list


def trim_reports(link_list):
    report_bool = []
    for link in link_list:
        report_bool.append(1)
    reports = list(zip(link_list, report_bool))
    report_list = pd.DataFrame(reports, columns=['Link', 'Report_Bool'])
    report_list = report_list[report_list.Report_Bool == 1]
    report_list.drop(['Report_Bool'], axis=1, inplace=True)
    report_list.drop_duplicates(keep='first', inplace=True)

    return report_list


def create_output_doc():
    columns = ['Title', 'Link', 'Summary', 'Analyst(s)', 'Published', 'Doc ID']
    dataframe = pd.DataFrame(columns=columns)
    return dataframe


def add_page_content(url, dataframe):
    soup = get_soup(url)

    title = soup.find('h1').text.strip()

    date = soup.find('p', class_='date').text.strip()
    date = date.replace(',', '')
    date = datetime.strptime(date, '%B %d %Y')
    date = datetime.strftime(date, '%d/%m/%Y')

    doc_id = url.split('-')[-1]

    analysts = soup.find_all('a', class_='primary-authors')
    analysts = [analyst.text.strip() for analyst in analysts]
    analysts = ', '.join(analysts)
    analysts = analysts.split(',')
    analyst = [x.strip() for x in analysts]
    analyst = ', '.join(analyst)

    summary = str(soup.find('div', class_='report-section').find_next('p').text.strip())

    new_row = {'Title': title, 'Published': date, 'Doc ID': doc_id, 'Analyst(s)': analyst,
               'Summary': summary, 'Link': url}
    return dataframe.append(new_row, ignore_index=True)


def visit_each_page(report_list, full_results):
    for link in report_list['Link']:
        full_results = add_page_content(link, full_results)
    return full_results


# ---- MAIN FUNCTION---- #
def get_csv(search_terms):

    results_df = create_output_doc()
    url_str = 'https://www.forrester.com/search?tmtxt=<Search_Term>&searchOption=10001&page=<Page_Num>&dateRange=2'
    link_list = []

    for search_term in search_terms:
        search_url = create_url(url_str, '1', search_term)
        search_soup = get_soup(search_url)

        link_list = get_doc_list(link_list, search_soup, url_str, search_term)

    report_list = trim_reports(link_list)
    results_df = results_df.append(visit_each_page(report_list, results_df))
    results_df.to_csv('forrester.csv', encoding='utf-8-sig', index=False)

    return results_df
