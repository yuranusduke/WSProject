# -*- coding: utf-8 -*-
"""
This file is the gate of the whole project

Created by Kunhong Yu
Date: 2022/04/26
"""
"""
In this project, I plan to crawl https://arxiv.org/
which is a large website that serves as like 'github' however,
it stores many research papers for public reading, there are many categories
in this website, for examples, the main page contains,
1. Physics
2. Mathematics
3. Computer Science
4. Quantitative Biology
5. Quantitative Finance
6. Statistics
7. Electrical Engineering and Systems Science
8. Economics
I plan to focus on these 8 subjects, and extract information for
each paper, in particular, for each subject, there are many kinds of
sub-subjects(ssubjects), and sub-sub-subject(sssubject) and each sssubject has link directing to all papers
related to this sssubject, and we can retrieve papers for each day(maximum is
5 days), therefore, and in this manner, I build scrapers to scrape
specific subject's sub-subject's sub-sub-subject's date's papers, extract information,
like, name of the paper, authors, abstracts, and subjects, and analyse them
using clustering and natural language processing(NLP) techniques.
"""
from fire import Fire
from soup.config import Config as BConfig
from soup.main import mainBS
from sscrapy.config import Config as SConfig
from sscrapy.main import mainScrapy
from sselenium.config import Config as SeConfig
from sselenium.main import mainSelenium
from fire import Fire
import time
from datetime import datetime

opt_bs = BConfig()
opt_scrapy = SConfig()
opt_selenium = SeConfig()

def main(**kwargs):
    model_name = input('Please choose model name : \n1. BeautifulSoup\n2. Scrapy\n3. Selenium\n')
    if model_name == '1': # soup
        string = '\n' + '*' * 20 + str(datetime.now()) + '*' * 20 + '\n'
        print('Parameters set: ')
        opt_bs.set_kwargs(**kwargs)
        string += opt_bs.print_kwargs()
        s = time.time()
        mainBS(opt_bs)
        e = time.time()
        print('Scraping and plotting approximately elapsed time : {:.2f}s.'.format(e - s))
        string += '*' * 50 + '\n'
        string += 'Elapsed time : ' + str(e - s) + 's.\n'

        with open('./records/bs_records.txt', 'a+') as f:
            f.write(string)
            f.flush()

    elif model_name == '2': # sscrapy
        string = '\n' + '*' * 20 + str(datetime.now()) + '*' * 20 + '\n'
        print('Parameters set: ')
        opt_scrapy.set_kwargs(**kwargs)
        string += opt_scrapy.print_kwargs()
        s = time.time()
        mainScrapy(opt_scrapy)
        e = time.time()
        print('Scraping and plotting approximately elapsed time : {:.2f}s.'.format(e - s))
        string += '*' * 50 + '\n'
        string += 'Elapsed time : ' + str(e - s) + 's.\n'

        with open('./records/scrapy_records.txt', 'a+') as f:
            f.write(string)
            f.flush()

    elif model_name == '3': # sselenium
        string = '\n' + '*' * 20 + str(datetime.now()) + '*' * 20 + '\n'
        print('Parameters set: ')
        opt_selenium.set_kwargs(**kwargs)
        string += opt_selenium.print_kwargs()
        s = time.time()
        mainSelenium(opt_selenium)
        e = time.time()
        print('Scraping and plotting approximately elapsed time : {:.2f}s.'.format(e - s))
        string += '*' * 50 + '\n'
        string += 'Elapsed time : ' + str(e - s) + 's.\n'

        with open('./records/selenium_records.txt', 'a+') as f:
            f.write(string)
            f.flush()

    else:
        raise Exception('No other models!')


# unit test
if __name__ == '__main__':
    """
    Usage:
        python main.py main \
            --subject=['Computer Science'] \
            --ssubject=['Computing Research Repository'] \
            --sssubject=['Computer Vision and Pattern Recognition'] \
            --limit=100 \
            --scrape_each_author=True \
            --crawl=True \
            --analyse=True 
    """
    Fire()

    print('\nDone!\n')
