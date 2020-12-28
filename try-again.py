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
    links = search_soup.find_all('a', class_='result-heading')
    for link in links:
        print(link.text)
        print(link['href'])


# url = create_url("https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>", '1', 'AI')

doc_page_url = 'https://www.gartner.com/en/documents/2020/12/3993877-predicts-2021-operational-ai-infrastructure-and' \
               '-enabling'

columns = ['Title', 'Date', 'Doc ID', 'Analyst(s)', 'Summary', 'Link']
results_df = pd.DataFrame(columns=columns)


def add_page_content(url, dataframe):

    soup = get_soup(url)

    title = soup.find('h1').text.strip()
    date = soup.find('span', string=re.compile('Published')).parent.text.strip()
    doc_id = soup.find('span', string=re.compile('ID')).parent.text.strip()
    analyst = soup.find('span', string=re.compile('Analyst')).parent.text.strip()
    summary = str(soup.find('h5').find_next('p').text.strip())

    new_row = {'Title': title, 'Date': date, 'Doc ID': doc_id, 'Analyst(s)': analyst, 'Summary': summary, 'Link': url}
    return dataframe.append(new_row, ignore_index=True)


results_df = add_page_content(doc_page_url, results_df)
print(results_df)
