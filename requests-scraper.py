import pandas as pd
import requests
from bs4 import BeautifulSoup

search_terms = ["AI", "Big Data", "Machine Learning"]  # To be looped over once we get it working


def create_url(url_str, page_num, search_term):
    url_str = url_str.replace('<Search_Term>', search_term)
    url_str = url_str.replace('<Page_Num>', page_num)
    return url_str


def get_num_results(soup):
    str_results = soup.find('div', class_='found-result col-xs-12').text  # find all strong tags in search-count
    str_results = str_results.strip()  # Remove all leftover spaces
    str_results = str_results.split(" ")[0]  # Remove everything after the space - leaving only the number of results
    num_results = int(str_results.replace(',', ''))
    return num_results


def get_search_soup(url, page_num, search_term):
    url = create_url(url, page_num, search_term)

    try:
        response = requests.get(url, timeout=(3, 10))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    else:
        print("Got connection")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup


def scrape_page(page):
    df_results = pd.DataFrame()
    titles = []
    report_ids = []
    summaries = []
    report_dates = []
    authors = []
    urls = []

    # set values to default empty string
    title = ''
    report_id = ''
    doc_url = ''
    sub_title = ''
    summary = ''
    report_date = ''
    author = ''
    report_bool = False

    # Is this item a report?
    if page.find('a', attrs={'class': 'result-heading'}) is not None:
        html_object = page.find('a', attrs={'class': 'result-heading'})
        doc_url = html_object['href']
        title = html_object.text
        if "/en/documents/" in doc_url:
            report_id = doc_url.replace("/en/documents/", "")
            doc_url = "https://www.gartner.com/en/documents/" + report_id
            report_bool = True

        if report_bool:
            # summary = get_summary('Gartner', doc_url)
            summary = 'Hello'
            if page.find('div', class_='item-category') is not None:
                html_objects = page.find_all('div', class_='item-category')
                for html_object in html_objects:
                    item_str = html_object.text
                    if "Analyst(s):" in item_str:
                        authors = item_str.replace('Analyst(s):', '')
                        authors = authors.replace('\n', '')
                        authors = authors.replace('|', ';')
                        authors = " ".join(authors.split())  # remove all leading, trailing and mid whitespace
                        authors = authors.replace(' ;', ';')
                    else:
                        spans = html_object.find_all('span', class_='mg-l6')
                        if len(spans) > 0:
                            report_date = spans[-1].text  # date is last of the span objects??

            summaries.append(summary)
            titles.append(title)
            report_ids.append(report_id)
            urls.append(doc_url)
            report_dates.append(report_date)
            authors.append(authors)

            df_results = pd.DataFrame({'ID': report_ids,
                                       'Title': titles,
                                       'Summary': summaries,
                                       'Report_Date': report_dates,
                                       'Authors': authors,
                                       'Url': urls})
    return df_results


def get_search_results(url, page_num, search_term):
    soup = get_search_soup(url, page_num, search_term)  # Change this to iterate over all pages?
    get_num_results(soup)

    page_num = '0'
    soup = get_search_soup(url, page_num, search_term)
    page_results = soup.find_all('div', class_='search-tem row')
    return page_results


class GartnerScraper(object):
    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.total_results = dict()
        self.url = "https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>"

    def save_page_data(self, dataframe):
        pass

    def return_dataframe(self):
        pass


# Testing code
gartner_scraper = GartnerScraper()
url = create_url("https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>", '1', 'AI')
page_res = get_search_results(url, '1', 'AI')
print(scrape_page(page_res))
