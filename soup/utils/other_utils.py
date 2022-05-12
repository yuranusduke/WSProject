# -*- coding: utf-8 -*-
"""Other utility functions

Created by Kunhong Yu(444447)
Date: 2022/03/24
"""
<<<<<<< HEAD
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
=======
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import requests
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8
headers = requests.utils.default_headers()
# to avoid blocked
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def getPage(url: str):
    """Get page from target url
    Args :
        --url: url
        --tag: target tag
    return :
        --soup: BeautifulSoup instance
    """
    try:
        # page = urlopen(url)
        page = requests.get(url, headers = headers) # avoid being blocked
        bs = BeautifulSoup(page.content, 'lxml') # we must use this to avoid broken-down page

        return bs

    except HTTPError as e:
        print(e)
        exit()
    except URLError as e:
        print(e)
        exit()


class WebModel(object):
    """Get website model"""

    def __init__(self, url, selector):
        """
        Args :
            --url: website url
            --selector: CSS selector
        """
        self.url = url
        self.selector = selector


def print_big_dict(big_dict, count):
    """
    Print big dict for scrape_utils.py
    Args :
        --big_dict
        --count
    """
    for subject, ssubjects in big_dict.items():
        for ssubject, sssubjects in ssubjects.items():
            for sssubject, links in sssubjects.items():
                print(subject + ':')
                print('\t' + ssubject + ':')
                print('\t\t' + sssubject + '-->')
                for link in links:
                    print('\t\t\t' + link)


    #         subs[ssubject] = ssubs
    #
    #     all_links[subject] = subs
    # values = list(big_dict.values())
    # if not values or isinstance(values[0], str) or isinstance(values[0], list):
    #     for k, v in big_dict.items():
    #         if isinstance(v, str):
    #             print('\t' * count + k + '-->' + v)
    #         elif isinstance(v, list):
    #             print('\t' * count + k + '-->')
    #             for vv in v:
    #                 print('\t' * count + vv)
    #
    #     return
    #
    # for k, v in big_dict.items():
    #     print('\t' * count + k + ':')
    #     time.sleep(0.2)
    #     print_big_dict(v, count + 1) # recursively print

class MyExpcetion(Exception):
    # my own exception
    def __init__(self):
        pass