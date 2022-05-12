# -*- coding: utf-8 -*-
"""
Similar to soup package, we have define crawl function to
do them automatically using sscrapy

Created by Kunhong Yu
Date: 2022/04/25
"""

from sscrapy.utils import *

# Finally, we combine them together
def crawl_all(limit = 50,
              scrape_each_author = True,
              page_limit = False,
              subject = ['Computer Science', 'Physics', 'Mathematics'],
              ssubject = ['Computing Research Repository', 'Physics', 'Mathematics'],
              sssubject = ['Computer Vision and Pattern Recognition', 'Machine Learning',
                          'Applied Physics', 'functional analysis']):
    """This function is used to combine all together
    Unlike Beautiful Soup, we can not print information SEQUENTIALLY,
    since scrapy runs with multithreads, so we tend to print each item
    after we scrape everything!
    Args :
        --limit: upper limit of scrapy, default is 50
        --page_limit: default is False, setting True will end the program when the number of scraped page is 100
        --subject: main subject
        --ssubject: subsubject
        --sssubject: subsubsubject
    return :
        --author_links
    """
    spider = ScrapySpider(limit = limit,
                          subject = subject,
                          ssubject = ssubject,
                          scrape_each_author = scrape_each_author,
                          page_limit = page_limit,
                          sssubject = sssubject)
    spider.spider()
    reactor.run()
    result = spider.result
    # 1. Get all links of subsubsubjects and each paper's information
    for s in result:
        for ss in result[s]:
            count = 0
            for sss in result[s][ss]:
                if len(result[s][ss][sss]) != 0:
                    for res in result[s][ss][sss]:
                        if not count:
                            print(f'{s} : ')
                            print(f'\t{ss} : ')
                            print(f'\t\t{sss} --> ')
                        print(f"\t\t\t{count + 1} : {res['title']}")
                        count += 1

    # 2. Then we need to go deeper with each author if necessary
    if scrape_each_author:
        print("\033[0;36;40mStarting scraping each author's information...\033[0m")
        # structure : {0 : [(0, 0), (1, 1), ...], ...}
        for name, _ in spider.author_links.items():
            print(f'\tAuthor : {name} --> ')
            count = 0
            try:
                for record_name, title in spider.author_dict[name]:
                    print(f'\t\tGetting {count + 1} paper name : {title.strip()}.')
                    if record_name.count(name):
                        print(f'\t\t\033[0;36;42mThis paper belongs to {name}.\033[0m')
                    count += 1
            except:
                pass

        print("\033[0;36;40mScraping each author's information is done!\033[0m")



# Unit test
if __name__ == '__main__':
    crawl_all(limit = 10,
              scrape_each_author = True,
              page_limit = True)