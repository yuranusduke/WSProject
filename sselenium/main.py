# -*- coding: utf-8 -*-
"""
Main function for sselenium

Created By Ludi Feng & Kunhong Yu
Date: 2022/05/12
"""
import sys
sys.path.append('../')
from sselenium.crawl import crawl_all
from processing.process import procedure

def mainSelenium(opt):
    # main function

    # we start crawling
    if opt.crawl:
        print('*' * 50)
        print('Start crawling using sselenium...')
        papers = crawl_all(limit = opt.limit, subject = opt.subject,
                           ssubject = opt.ssubject, sssubject = opt.sssubject,
                           page_limit = opt.page_limit)
        print(papers)

    if opt.analyse:
        # if analyses all information
        print('*' * 50)
        print('Start analysing...')
        procedure(mode = 'sselenium', for_author = False)
        print('*' * 50)

    print('*' * 50)


## unit test
if __name__ == '__main__':
    from sselenium.config import Config as Seconfig
    opt_selenium = Seconfig()
    opt_selenium.analyse = False
    mainSelenium(opt_selenium)