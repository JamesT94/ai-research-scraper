import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def create_url(url_str, page_num, search_term):
    url_str = url_str.replace('<Search_Term>', search_term)
    url_str = url_str.replace('<Page_Num>', page_num)
    return url_str


def get_soup(url):
    response = 0
    try:
        response = requests.get(url, timeout=(3, 10))
        print('Got a connection to {}'.format(url))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)

    result_soup = BeautifulSoup(response.text, 'html.parser')
    return result_soup


def get_doc_list(search_soup):
    results = []
    links = search_soup.find_all('a', class_='result-heading')
    for link in links:
        results.append(link['href'])
    return results


def trim_reports(link_list, report_bool):
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
    columns = ['Title', 'Date', 'Doc ID', 'Analyst(s)', 'Summary', 'Link']
    dataframe = pd.DataFrame(columns=columns)
    return dataframe


def add_page_content(url, dataframe):

    soup = get_soup(url)

    title = soup.find('h1').text.strip()
    date = soup.find('span', string=re.compile('Published')).parent.text.strip()
    doc_id = soup.find('span', string=re.compile('ID')).parent.text.strip()
    analyst = soup.find('span', string=re.compile('Analyst')).parent.text.strip()
    summary = str(soup.find('h5').find_next('p').text.strip())

    new_row = {'Title': title, 'Date': date, 'Doc ID': doc_id, 'Analyst(s)': analyst, 'Summary': summary, 'Link': url}
    return dataframe.append(new_row, ignore_index=True)


def visit_each_page(report_list, full_results):
    for link in report_list['Link']:
        full_results = add_page_content(link, full_results)
    return full_results


search_url = create_url("https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>", '1', 'AI')

results_df = create_output_doc()

search_soup = get_soup(search_url)

link_list = get_doc_list(search_soup)

report_bool = []
report_list = trim_reports(link_list, report_bool)

results_df = visit_each_page(report_list, results_df)
results_df.to_csv('output.csv')







