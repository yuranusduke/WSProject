# -*- coding: utf-8 -*-
"""Other utility functions

Created by Kunhong Yu(444447)
Date: 2022/04/20
"""
from scrapy import signals
from scrapy.signalmanager import dispatcher
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import requests
headers = requests.utils.default_headers()
# to avoid blocked
headers.update({
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
})
proxies = {"http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.10:1080"}


def getPage(url: str):
    """Get page from target url
    Args :
        --url: url
        --tag: target tag
    return :
        --soup: BeautifulSoup instance
    """
    try:
        page = requests.get(url, headers = headers)
        # from: https://stackoverflow.com/questions/43440397/requests-using-beautiful-soup-gets-blocked
        bs = BeautifulSoup(page.content, 'lxml') # we must use this to avoid broken-down page

        return bs

    except HTTPError as e:
        print(e)
        exit()
    except URLError as e:
        print(e)
        exit()

def print_big_dict(big_dict):
    """
    Print big dict for scrape_utils.py
    Args :
        --big_dict
    """
    for subject, ssubjects in big_dict.items():
        for ssubject, sssubjects in ssubjects.items():
            for sssubject, links in sssubjects.items():
                print(subject + ':')
                print('\t' + ssubject + ':')
                if isinstance(links, list):
                    print('\t\t' + sssubject + '-->')
                    for link in links:
                        print('\t\t\t' + link)
                else:
                    print('\t\t' + sssubject + ' : ' + links)

class MyExpcetion(Exception):
    # my own exception
    def __init__(self):
        pass


def spider_results(MySpider, process, results, s, ss, sss, **kwargs):
    """This function is used to get spider results
    Code from: https://stackoverflow.com/questions/40237952/get-scrapy-crawler-output-results-in-script-file-function
    Args :
        --MySpider: My built spider instance
        --process: CrawlerRunner instance
    return :
        --results: Python list
    """

    def crawler_results(signal, sender, item, response, spider):
         results[s][ss][sss] = item

    dispatcher.connect(crawler_results, signal = signals.item_scraped)

    process.crawl(MySpider, **kwargs)

    return results