# -*- coding: utf-8 -*-
"""
This file is used to crawl from a specific paper to all papers related to the
author using soup. Note that we don't consider page limit when we need to scrape each
author's information, in particular, we only consider number of pages when papers belongings to
that author.
Also, there is a possibility that under your specificity of
subsubsubjects, there are no 100 pages, so the result is less than 100.

Created by Kunhong Yu
Date: 2022/04/20
"""
from soup.utils import LinkScraper, InfoScraper
from soup.utils import print_big_dict
import pandas as pd
from soup.utils import AuthorsScraper


def crawl_all(subject = 'Computer Science',
              ssubject = 'Computing Research Repository',
              sssubject = 'Computer Vision and Pattern Recognition',
              limit = 50,
              page_limit = False,
              get_all = False,
              scrape_each_author = False):
    """This function is used to crawl all information and store them
    Args :
        --subject: main subject, type is str or list
        --ssubject: sub-subject, type is str or list
        --sssubject: sub-sub-subject, type is str or list
        --limit: number of papers to extract, default is 50
                    --page_limit: default is False, setting True will end the program when the number of scraped page is 100
        --get_all: if True, scrape all subject's information regardless of subject, ssubject and
            sssubject, try not to use this !!!!
        --scrape_each_author: True to scrape all authors information
    """

    # 1. First, we need to scrape all pages' information and store them,
    # which is done via utils
    print('\033[0;36;40mStarting scraping papers...\033[0m')
    if page_limit:
        limit = 100
    scraper = LinkScraper(subject = subject,
                          ssubject = ssubject,
                          sssubject = sssubject,
                          limit = limit,
                          get_all = get_all)
    all_links, all_author_links = scraper.scrape_paper_links()
    print_big_dict(all_links, 0)
    print('\033[0;36;40mScraping papers links is done!\033[0m\n')
    assert isinstance(all_links, dict)

    print("\033[0;36;40mStarting scraping papers's information...\033[0m")
    df = pd.DataFrame({'title': [], 'authors': [], 'abstract': [],
                       'comment': [], 'subject' : [], 'subsubject' : [], 'subsubsubject' : []})
    flag = False # set flag break
    for subject, ssubjects in all_links.items():
        for ssubject, sssubjects in ssubjects.items():
            for sssubject, papers_links in sssubjects.items():
                print('subject:', subject)
                print('\tssubject:', ssubject)
                print('\t\tsssubject:', sssubject)
                info_scrape = InfoScraper(links = papers_links, page_limit = page_limit)
                df = info_scrape.scrape_info(df, subject, ssubject, sssubject)
                if page_limit and len(df) >= 100:
                    print('Upper limit 100 papers are scraped!')
                    flag = True
                    break
            if flag:
                break

        if flag:
            break

<<<<<<< HEAD
    try:
        df.to_csv('./soup/data/allinfo.csv', index = False, sep = '#')
    except:
        df.to_csv('./data/allinfo.csv', index = False, sep = '#')
=======
    df.to_csv('./soup/data/allinfo.csv', index = False, sep = '#')
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8
    print("\033[0;36;40mScraping papers's information is done, saved in /data/allinfo.csv!\033[0m\n")

    # 2. Then we need to go deeper with each author if necessary
    if scrape_each_author:
        print("\033[0;36;40mStarting scraping each author's information...\033[0m")
        df = pd.DataFrame({'name': [], 'title': [], 'abstract': []})
        authorscraper = AuthorsScraper(all_author_links, page_limit = page_limit)
        df = authorscraper.scrape(df)
<<<<<<< HEAD
        try:
            df.to_csv('./soup/data/allauthorsinfo.csv', index = False, sep = '#')
        except:
            df.to_csv('./data/allauthorsinfo.csv', index = False, sep = '#')
=======
        df.to_csv('./soup/data/allauthorsinfo.csv', index = False, sep = '#')
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8


# unit test
# if __name__ == '__main__':
#     crawl_all(subject = ['Computer Science', 'Physics', 'Mathematics'],
#               ssubject = ['Computing Research Repository', 'Physics', 'Mathematics'],
#               sssubject = ['Computer Vision and Pattern Recognition', 'Machine Learning', 'Applied Physics', 'functional analysis'],
#               limit = 100,
#               get_all = False,
#               scrape_each_author = True)