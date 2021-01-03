"""
Need to update to search for other terms and only add the row if it doesn't already exist
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime


def create_url(url_str, page_num, search_term):
    search_term = search_term.replace(" ", "%20")
    url_str = url_str.replace('<Search_Term>', search_term)
    url_str = url_str.replace('<Page_Num>', page_num)
    return url_str


def get_soup(url):
    response = 0
    try:
        response = requests.get(url, timeout=(3, 10))
        print('Got a connection to {}'.format(url))
    except requests.exceptions.RequestException as e:
        print(e)

    result_soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    return result_soup


def get_doc_list(first_search_soup, url_str, search_term):
    num_pages = first_search_soup.find('div', class_='found-result col-xs-12').text.strip()
    num_pages = int(num_pages.split(' ')[-1])

    link_list = []
    for page in range(1, num_pages + 1):
        url = create_url(url_str, str(page), search_term)
        soup = get_soup(url)
        links = soup.find_all('a', class_='result-heading')
        for link in links:
            link_list.append(link['href'])

    return link_list


def trim_reports(link_list):
    report_bool = []
    substring = '/en/documents/'
    for link in link_list:
        if substring in link:
            report_bool.append(1)
        else:
            report_bool.append(0)
    reports = list(zip(link_list, report_bool))
    report_list = pd.DataFrame(reports, columns=['Link', 'Report_Bool'])
    report_list = report_list[report_list.Report_Bool == 1]
    report_list.drop(['Report_Bool'], axis=1, inplace=True)

    return report_list


def create_output_doc():
    columns = ['Title', 'Link', 'Summary', 'Analyst(s)', 'Published', 'Doc ID']
    dataframe = pd.DataFrame(columns=columns)
    return dataframe


def add_page_content(url, dataframe):
    soup = get_soup(url)

    title = soup.find('h1').text.strip()

    date = soup.find('span', string=re.compile('Published')).parent.text.strip()
    date = date.split(': ')[1]
    date = datetime.strptime(date, '%d %B %Y')
    date = datetime.strftime(date, '%d/%m/%Y')

    doc_id = soup.find('span', string=re.compile('ID')).parent.text.strip()
    doc_id = doc_id.split(': ')[1]

    analyst = soup.find('span', string=re.compile('Analyst')).parent.text
    analyst = re.sub('\s+', ' ', analyst).split(':')[1]
    analyst = analyst.split(',')
    analyst = [x.strip() for x in analyst]
    analyst = ', '.join(analyst)

    summary = str(soup.find('h5').find_next('p').text.strip())

    new_row = {'Title': title, 'Published': date, 'Doc ID': doc_id, 'Analyst(s)': analyst,
               'Summary': summary, 'Link': url}
    return dataframe.append(new_row, ignore_index=True)


def visit_each_page(report_list, full_results):
    for link in report_list['Link']:
        full_results = add_page_content(link, full_results)
    return full_results


# ---- MAIN ---- # TURN ALL THIS INTO A NICE FUNCTION SO IN THE OTHER FILE YOU DON'T DO MUCH
url_str = 'https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>'
search_url = create_url(url_str, '1', 'machine learning')
search_soup = get_soup(search_url)

link_list = get_doc_list(search_soup, url_str, 'machine learning')
report_list = trim_reports(link_list)

results_df = create_output_doc()
results_df = visit_each_page(report_list, results_df)
results_df.to_csv('output.csv', encoding='utf-8-sig', index=False)
