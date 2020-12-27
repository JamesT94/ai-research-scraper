

import requests
from requests.exceptions import Timeout
import urllib.request
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
# import pandas_profiling
import math
import os

# Forrester search - last 12 months only and only reports
FORRESTER_URL = 'https://www.forrester.com/search?tmtxt=<Search_Term>&searchOption=10001&page=<Page_Num>&dateRange=2'

# IDC search - Last 12 months English only, Insights-Only research, Presentations, briefs, Studies,
# Top 10 Predictions, Product Information, Event Proceedings
IDC_URL = 'https://www.idc.com/search/advanced/perform_.do?page=<Page_Num>&hitsPerPage=25&sortBy=RELEVANCY&lang' \
          '=English&srchIn=ALLRESEARCH&src=&athrT=10&aq=<Search_Term>&aq=&aq=&aq=&op=ALL&op=ANY&op=EXCLUDE&op=EXACT' \
          '&in=EVERYWHERE&in=EVERYWHERE&in=EVERYWHERE&in=EVERYWHERE&lp=1&lpr=1Y&cg=5_1288&cg=5_1290&cg=5_1282&cg' \
          '=5_1293&cg=5_1294&cg=5_1292&cg=5_1285&cmpT=10&pgT=10&trid=72228738&ptrid=72228627&siteContext=IDC '

# Gartner search - can only specify search term and page number
GARTNER_URL = "https://www.gartner.com/en/search?keywords=<Search_Term>&page=<Page_Num>"


def sentence_case(input_str):
    # Capitalize method returns a copy of the string with only its first character capitalized.
    str_result = '. '.join(i.capitalize() for i in input_str.split('. '))
    str_result.replace(' ceos', ' CEOs ')
    str_result.replace(' ceo', ' CEO ')
    str_result.replace(' cios ', ' CIOs ')
    str_result.replace(' cio ', ' CIO ')
    str_result.replace(' dell ', ' Dell ')
    str_result.replace(' ai ', ' AI ')
    str_result.replace(' iot ', ' IoT ')
    return str_result


def create_url(url_str, page_num, search_term):
    url_str = url_str.replace('<Search_Term>', search_term)
    url_str = url_str.replace('<Page_Num>', page_num)
    return url_str


def convert_str_int(temp_str):
    temp_str = temp_str.replace(',', '')
    temp_int = int(temp_str)
    return temp_int


# Get number of results
def find_IDC_results(soup):
    # strong_tags_total = soup.find('div', id = 'search-count').find_all('strong') #find all strong tags in search-count
    str_results = soup.find('div', class_='results-header__count').text
    # Remove leading spaces
    str_results = str_results.strip()
    # Remove everything after the space - leacing only the number of results
    str_results = str_results.split(" ")[0]
    # str_results = strong_tags_total[1].text  #we want the text of the second strong tag
    num_results = convert_str_int(str_results)
    return num_results


# Get number of results
def find_Gartner_results(soup):
    # str_results = soup.find('div', class_ = 'found-result col-xs-12 unset-sidepaddings').text #find all strong tags
    # in search-count
    str_results = soup.find('div', class_='found-result col-xs-12').text  # find all strong tags in search-count
    # Remove leading spaces
    str_results = str_results.strip()
    # Remove everything after the space - leaving only the number of results
    str_results = str_results.split(" ")[0]
    num_results = convert_str_int(str_results)
    return num_results


# Get number of results
# Revise this so that we look for strong tags, ie like the find_IDC_results???
def find_Forrester_results(soup):
    result_total = soup.find('div', class_='result-total')
    str_results = result_total.strong.text
    str_results = str_results.replace(' results', '')
    num_results = convert_str_int(str_results)
    return num_results


def calc_num_pages(num_results, results_per_page):
    num_pages = math.ceil(num_results / results_per_page)
    return num_pages


def get_summary(provider_str, url):
    result = ""

    try:
        response = requests.get(url, timeout=(3, 10))
    except Timeout:
        print('The request for url' + url + 'timed out.')
    else:
        soup = BeautifulSoup(response.text, "html.parser")

        if provider_str == 'Gartner':
            if soup.find(attrs={'name': 'description'}) is not None:
                result = soup.find(attrs={'name': 'description'})['content']
        elif provider_str == 'IDC':
            if soup.find('div', class_='getdoc__main row large-unite-2-reversed unite-box') is not None:
                result = soup.find('div', class_='getdoc__main row large-unite-2-reversed unite-box').find('p').text
        else:
            if soup.find("div", {"id": "why-read"}) is not None:
                result = soup.find("div", {"id": "why-read"}).find('p').text
    return result


def get_Forrester_page_result(results_container):
    Titles = []
    Report_IDs = []
    Summaries = []
    Report_Dates = []
    Authors = []
    Urls = []

    for container in results_container:
        Title = container.a.text
        Titles.append(Title)

        ID = container.find('a', attrs={'class': 'title'})['data-uniqueid']
        Report_IDs.append(ID)

        doc_url = container.find('a', attrs={'class': 'title'})['href']
        doc_url = "https://www.forrester.com" + doc_url
        Urls.append(doc_url)

        summary = ''
        summary = get_summary('Forrester', doc_url)
        # if container.find('p', class_ = 'description') is not None:
        #    summary = container.find('p', class_ = 'description').text
        Summaries.append(summary)

        report_date = container.find('span', class_='date').text
        Report_Dates.append(report_date)

        analyst_names = ''
        names = []
        analysts = container.find_all('a', class_='analyst-name')
        for analyst in analysts:
            names.append(analyst.text)

        analyst_names = ";".join(names)

        Authors.append(analyst_names)

    df_results = pd.DataFrame({'ID': Report_IDs,
                               'Title': Titles,
                               'Summary': Summaries,
                               'Report_Date': Report_Dates,
                               'Authors': Authors,
                               'Url': Urls})
    return df_results


def get_IDC_page_result(results_container):
    print("IDC")
    Titles = []
    Report_IDs = []
    Summaries = []
    Report_Dates = []
    Authors = []
    Urls = []

    for container in results_container:
        # Title = container.h3.text
        # Titles.append(Title)

        html_object = container.find('a', attrs={'class': 'result-title'})
        # doc_url = html_object['href']
        Title = html_object.text
        # Remove leading spaces
        Title = Title.strip()
        Titles.append(Title)

        ID = container.find('a', attrs={'class': 'result-title'})['href']
        # Remove /url.do?url=/getdoc.jsp?containerId=
        ID = ID.replace("/url.do?url=/getdoc.jsp?containerId=", "")
        # Remove everything after the & sign leaving only the ID
        ID = ID.split("&")[0]
        Report_IDs.append(ID)

        doc_url = "https://www.idc.com/getdoc.jsp?containerId=" + ID
        Urls.append(doc_url)

        summary = ''
        if container.find('div', class_='result-synopsis') is not None:
            summary = container.find('div', class_='result-synopsis').text
            summary = summary.replace('\n', '')
            summary = summary.replace('&apos;s', "'s")
            summary = summary.replace("\ 's", "'s")

        Summaries.append(summary)

        report_date = ''
        if container.find('strong', class_='doc-date') is not None:
            report_date = container.find('strong', class_='doc-date').text
        Report_Dates.append(report_date)

        authors = ''
        if container.find('div', class_='result-authors') is not None:
            authors = container.find('div', class_='result-authors').text
            authors = authors.replace('\n', "")
            authors = authors.replace(',', ';')
            authors = " ".join(authors.split())  # remove all leading, trailing and mid whitespace
            authors = authors.strip()

        Authors.append(authors)

    df_results = pd.DataFrame({'ID': Report_IDs,
                               'Title': Titles,
                               'Summary': Summaries,
                               'Report_Date': Report_Dates,
                               'Authors': Authors,
                               'Url': Urls})
    return df_results


def get_Gartner_page_result(results_container):
    Titles = []
    Report_IDs = []
    Summaries = []
    Report_Dates = []
    Authors = []
    Urls = []

    for container in results_container:

        # set values to default empty string
        title = ""
        ID = ""
        doc_url = ""
        sub_title = ''
        summary = ''
        report_date = ""
        authors = ''
        report_bool = False

        if container.find('a', attrs={'class': 'result-heading'}) is not None:
            html_object = container.find('a', attrs={'class': 'result-heading'})
            doc_url = html_object['href']
            title = html_object.text
            if "/en/documents/" in doc_url:
                ID = doc_url.replace("/en/documents/", "")
                doc_url = "https://www.gartner.com/en/documents/" + ID
                report_bool = True

        if report_bool:

            summary = get_summary('Gartner', doc_url)

            # if container.find('div', class_ = 'result-text') is not None:
            #    html_object = container.find('div', class_ = 'result-text')
            #    summary = html_object.text
            #    summary = summary.replace('\n','')
            #    summary = bytes(summary, 'utf-8').decode('utf-8', 'ignore')
            #    summary = " ".join(summary.split()) #remove all leading, trailing and mid whitespace
            #    summary = sentence_case(summary)

            if container.find('div', class_='item-category') is not None:
                html_objects = container.find_all('div', class_='item-category')
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

            Summaries.append(summary)
            Titles.append(title)
            Report_IDs.append(ID)
            Urls.append(doc_url)
            Report_Dates.append(report_date)
            Authors.append(authors)

    # Fill data-frame
    df_results = pd.DataFrame({'ID': Report_IDs,
                               'Title': Titles,
                               'Summary': Summaries,
                               'Report_Date': Report_Dates,
                               'Authors': Authors,
                               'Url': Urls})
    return df_results


def get_research_df(provider_str, provider_url, results_per_page, provider_container_str, search_terms):
    for term in search_terms:

        if provider_str == 'Gartner':
            term = term.replace(" ", "%20")
        else:
            term = term.replace(" ", "+")

        # Go to page 1 of url site
        url = create_url(provider_url, '1', term)
        print(url)

        # You can also pass a tuple to timeout with the first element being a connect timeout (the time it allows for
        # the client to establish a connection to the server), and the second being a read timeout (the time it will
        # wait on a response once your client has established a connection):
        try:
            response = requests.get(url, timeout=(3, 10))
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
        # sys.exit(1)
        except Timeout:
            print('The request for url' + url + 'timed out.')
        else:
            print("Got connection")
            soup = BeautifulSoup(response.text, "html.parser")

            num_results = 0
            if provider_str == 'Gartner':
                num_results = find_Gartner_results(soup)
            elif provider_str == 'IDC':
                num_results = find_IDC_results(soup)
            else:
                num_results = find_Forrester_results(soup)

            if num_results > 0:

                num_pages = calc_num_pages(num_results, results_per_page)

                # for page_num in range(1, 3):
                # Should be num_pages + 1 but need to check page then exists
                for page_num in range(1, num_pages):
                    # Empty results container
                    results_container = None

                    url = create_url(provider_url, str(page_num), term)
                    print(url)
                    response = requests.get(url, timeout=(3, 10))
                    try:
                        response = requests.get(url, timeout=(3, 10))
                    except requests.exceptions.RequestException as e:  # This is the correct syntax
                        print(e)
                    except Timeout:
                        print('The request for url' + url + 'timed out.')
                    else:
                        soup = BeautifulSoup(response.text, "html.parser")
                        results_container = soup.find_all('div', class_=provider_container_str)

                        # Create empty data-frame
                        page_df = pd.DataFrame()
                        if len(results_container) > 0:
                            # Get results from provider page
                            if provider_str == 'Gartner':
                                page_df = get_Gartner_page_result(results_container)
                            elif provider_str == 'IDC':
                                page_df = get_IDC_page_result(results_container)
                            else:
                                page_df = get_Forrester_page_result(results_container)

                            page_df['Search_Term'] = term
                            page_df['Download_Date'] = datetime.today().strftime('%Y%m%d')
                            page_df['Provider'] = provider_str

                            file_path = r'../' + provider_str + r'_' + datetime.today().strftime('%Y%m%d') + r'.csv'

                            # if file does not exist write header 
                            if not os.path.isfile(file_path):
                                page_df.to_csv(file_path, header='column_names')
                            else:  # else it exists so append without mentioning the header
                                page_df.to_csv(file_path, mode='a', header=False)

        # Drop duplicate rows from data-frame, keeping first occurence, when unique rows are determined by ID
        # Ah - this doesn't quite work - removes also all records where ID is blank or manually set to None. keep those?


    # results_df.drop_duplicates(subset='ID', keep='first', inplace=True)

    # results_df

if __name__ == '__main__':
    search_terms = ['machine learning', 'big data', 'artificial intelligence']
    # search_terms = ['artificial intelligence']

    # Forrester has 25 results per page
    # Forrester works as at 4 March 2020 - omit for now whilst testing Gartner and IDC
    container_str = 'result-info'
    Forrester_df = get_research_df("Forrester", FORRESTER_URL, 25, container_str, search_terms)

    # Gartner has 20 results per page
    container_str = 'search-item row'
    Gartner_df = get_research_df("Gartner", GARTNER_URL, 20, container_str, search_terms)

    # IDC has 25 results per page
    # IDC works as at 4 March 2020 - omit for now whilst testing Gartner and IDC
    container_str = 'result-content'
    IDC_df = get_research_df("IDC", IDC_URL, 25, container_str, search_terms)

    # df_frames = [IDC_df]
    df_frames = [Forrester_df, Gartner_df, IDC_df]

    all_results = pd.concat(df_frames, ignore_index=True)

    all_results.to_csv('C:/Users/James/Desktop/Research_Scraping/Results/Research_Results_20201207.csv')

# all_results.to_csv(r'D:/Users/Calum/Documents/Capgemini/Forrester/Research_Results.csv')
