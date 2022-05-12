# -*- coding: utf-8 -*-
"""
Main function for soup

Created By Kunhong Yu(444447)
Date: 2022/04/26
"""
import sys
sys.path.append('../')
from soup.crawl import crawl_all
from processing.process import procedure


def mainBS(opt):
    # main function

    # we start crawling
    if opt.crawl:
        print('*' * 50)
        print('Start crawling using BeautifulSoup...')
        crawl_all(subject = opt.subject,
                  ssubject = opt.ssubject,
                  sssubject = opt.sssubject,
                  limit = opt.limit,
                  page_limit = opt.page_limit,
                  get_all = False, # I set it to False, since it's dangerous to scrape all information
                  scrape_each_author = opt.scrape_each_author)

    if opt.analyse:
        # if analyses all information
        print('*' * 50)
        print('Start analysing...')
        if opt.scrape_each_author:
            procedure(mode = 'soup', for_author = False) # for all the papers
            procedure(mode = 'soup', for_author = True) # for all the authors
        else:
            procedure(mode = 'soup', for_author = False)
        print('*' * 50)

    print('*' * 50)



## unit test
if __name__ == '__main__':
    from soup.config import Config as BConfig
    opt_bs = BConfig()
    opt_bs.analyse = False
    mainBS(opt_bs)