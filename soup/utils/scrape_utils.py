"""
This file contains utilities for scraping functions

Created by Kunhong Yu(444447)
Date: 2022/03/24 ~ 2022/05/02
"""
from soup.utils.other_utils import *
import traceback
import time
import itertools

from argparse import ArgumentParser

class LinkScraper(object):
    """Define link scraper class"""
    def __init__(self,
                 subject : str or list,
                 ssubject : str or list,
                 sssubject : str or list,
                 limit = 50,
                 get_all = False):
        """
        Args :
            --subject: main subject, type is str or list
            --ssubject: sub-subject, type is str or list
            --sssubject: sub-sub-subject, type is str or list
            --limit: number of papers to extract, default is 50
            --get_all: if True, scrape all subject's information regardless of subject, ssubject and
                sssubject
        """
        if isinstance(subject, str):
            subject = [subject]

        subject = [s.lower() for s in subject] # more robust
        self.subject = subject

        if isinstance(ssubject, str):
            ssubject = [ssubject]
        ssubject = [s.lower() for s in ssubject] # more robust
        self.ssubject = ssubject

        if isinstance(sssubject, str):
            sssubject = [sssubject]
        sssubject = [s.lower() for s in sssubject] # more robust
        self.sssubject = sssubject

        self.limit = limit
        # self.base_url = 'http://xxx.itp.ac.cn'
        self.base_url = 'https://arxiv.org'
        self.get_all = get_all

    def scrape_main_page(self):
        """This function is used to scrape main(first) page of the
        arxiv website: https://arxiv.org/ to find all subjects we need
        to extract links to each subject
        In the main page, all subjects are lying in the scope of <h2> of
        <main>
        """
        try:
            bs = getPage(url = self.base_url)
            subjects = bs.find('div', id = 'content').find_all('h2')
            # we must make program more robust
            # subjects = [subject for subject in subjects if
            #             subject.text.lower() in self.subject]

            big_dict = {} # we store all links to this big dictionary
            for subject in subjects: # subject
                # in the page, all links to other subsubjects are below
                # in the subject <h2> within unordered list <ul>
                ul = subject.find_next('ul')
                lis = ul.find_all('li')
                ss_dict = {}
                for li in lis: # sub-subject
                    ssubject = li.find('a') # get the name of the subsubject
                    ss_text = ssubject.text.lower()
                    # we aim to find sub-sub-subject's link

                    sss_dict = {}
                    try:
                        sssubject = li.find('br').next_siblings
                        sssubject = [x for x in sssubject if x.find('a') != -1] # find <a>
                        for sss in sssubject: # sub-sub-subject
                            sss_text = sss.text.lower()
                            if sss_text.count('detailed description'): # bug here
                                continue
                            url = self.base_url + sss.attrs['href']
                            sss_dict[sss_text] = url
                    except:
                        pass#print(ss_text)

                    ss_dict[ss_text] = sss_dict

                big_dict[subject.text.lower()] = ss_dict

            self.big_dict = big_dict

        except Exception as e:
            traceback.print_exc()


    def scrape_specific_page(self, link):
        """
        This function is used to scrape a specific page using given link
        to get all paper's links, in particular, the link lies in <dl> --> <dt> -- >
        <span> --> <a>
        Args :
            --link: input link
        return :
            --links: all paper's link, upper limit is `limit`
        """
        links = []
        author_links = {}
        def __one_page(link, links):
            """This inside function is used to scrape a single page papers
            Args :
                --link: single pager link
                --links: current paper links
            return :
                --links: all papers' links to current page
                --author_links
                --soup
            """
            bs = getPage(url = link)
            try:
                days = bs.find_all('dl')
                links = []
                author_links = {}
                count = 0
                for day in days:
                    link_day = []
                    papers = day.find_all('dt')
                    authors = day.find_all('dd')
                    for paper, author in zip(papers, authors):
                        single_link = paper.find('span', class_ = 'list-identifier').find('a').attrs['href']
                        # to find author link
                        author_link = author.find('div', class_ = 'list-authors').find('a') # find only first author
                        author = author_link.text.strip()
                        author_link = author_link.attrs['href']
                        author_links.update({author : self.base_url + author_link})
                        link_day.append(self.base_url + single_link)
                        count += 1
                    links.extend(link_day)
                return links, author_links, bs

            except:
                traceback.print_exc()
                return [], {}, bs

        cur_links, cur_author_links, bs = __one_page(link = link, links = links)
        author_links.update(cur_author_links)
        links.extend(cur_links)
        if len(links) < self.limit:
            # turn to another page
            # first, we need to check if there is another page,
            # since original arxiv finds 25 papers each page,
            # We have to separate situations
            tags = list(filter(lambda x: x.get_text().startswith('[ total of '), bs.find_all('small')))
            tags = tags[0]
            if not tags.find('a'): # only less 25 papers found
                print(f'There are only {len(links)} papers in this subject!')
            else:  # multiple pages
                all_other_pages = tags.find_all('a') # other pages, !!!
                page_links = [self.base_url + page_link.attrs['href'] for page_link in all_other_pages]
                for page_link in page_links:
                    cur_links, cur_author_links, bs = __one_page(link = page_link, links = links)
                    links.extend(cur_links)
                    author_links.update(cur_author_links)

                    if len(links) >= self.limit:
                        return links[:self.limit], dict(itertools.islice(author_links.items(), self.limit)) # slice a dictionary

                # one more logic is if limit is too large, then we only scrape upper
                # upper limit in the arixv page

        else:
            return links[:self.limit], dict(itertools.islice(author_links.items(), self.limit))

        return links, author_links


    def scrape_paper_links(self):
        """This function is used to scrape all paper links using above two methods
        return :
            --all_links: all returned links using dictionary
            --all_author_links
        """
        # 1. scrape main page
        self.scrape_main_page()
        # 2. scrape specific page and return all papers' links
        all_links = {}
        all_author_links = {}
        if self.get_all:
            for subject, ssubjects in self.big_dict.items():
                subs = {}
                for ssubject, sssubjects in ssubjects.items():
                    ssubs = {}
                    for sssubject, link in sssubjects.items():
                        try: # to deal with wrong categories
                            links, author_links = self.scrape_specific_page(link = link)
                            ssubs[sssubject] = links
                            all_author_links.update(author_links)
                        except:
                            # traceback.print_exc()
                            pass

                    subs[ssubject] = ssubs

                all_links[subject] = subs
        else:
            for subject in self.subject:
                subs = {}
                for ssubject in self.ssubject:
                    ssubs = {}
                    for sssubject in self.sssubject:
                        try: # to deal with wrong categories
                            link = self.big_dict[subject][ssubject][sssubject]
                            links, author_links = self.scrape_specific_page(link = link)
                            ssubs[sssubject] = links
                            all_author_links.update(author_links)
                        except:
                            # traceback.print_exc()
                            pass

                    subs[ssubject] = ssubs

                all_links[subject] = subs

        return all_links, all_author_links


class InfoScraper(object):
    """Define information scraper"""
    def __init__(self, links, page_limit = False):
        """
        Args :
            --link: ONE paper's link
                        --page_limit: default is False, setting True will end the program when the number of scraped page is 100
        """
        self.links = links
        self.page_limit = page_limit

    def scrape_single_info(self, bs):
        """
        Scrape information in single paper page
        We can get title, authors, abstract and comment of the paper.
        Where title is in <h1 class = 'title mathjax'>
        authors are in <div class = 'authors'>
        abstract is in <blockquote class = 'abstract mathjax'>
        comment is in first <tr> of <table summary = 'Addition metadata'>
        Args :
            --soup: single paper BeautifulSoup instance
        return :
            --res: dictionary to store all information we scraped
        """
        res = {}
        try: # find title
            title = bs.find('h1', class_ = 'title mathjax').text
        except:
            print("\t\t\t\tCan't find title, please check!")
            title = ""
        res['title'] = title.strip().lstrip('Title').lstrip(':').lstrip('"').rstrip('"').strip()

        try: # find authors
            authors = bs.find('div', class_ = 'authors').text
        except:
            # print("\t\t\t\tCan't find authors, please check!")
            authors = "" # Be careful with lstrip function!
        res['authors'] = authors.strip().lstrip('Authors').lstrip(':')

        try: # find abstract
            abstract = bs.find('blockquote', class_ = 'abstract mathjax').text
        except:
            # print("\t\t\t\tCan't find abstract, please check!")
            abstract = ""
        res['abstract'] = abstract.strip().lstrip('Abstract').lstrip(':').lstrip('"').rstrip('"').strip()

        try: # find comment
            table = bs.find('table', {'summary' : 'Additional metadata'})
            comment = table.find('tr').text
            if comment.count('Comments:') == 0:
                raise MyExpcetion()
        except:
            # print("\t\t\t\tCan't find comment, please check!")
            comment = ""
        res['comment'] = comment.strip().lstrip('Comments').lstrip(':').lstrip('"').rstrip('"').strip()

        return res

    def scrape_info(self, df, subject, ssubject, sssubject):
        """Scrape all links' information
        Args :
            --df: data frame
            --subject, ssubject, sssubject
        return :
            --df
        """
        for i, link in enumerate(self.links):
            try:
                bs = getPage(url = link)
                res = self.scrape_single_info(bs = bs)

                #time.sleep(0.2)
                res['subject'] = subject
                res['subsubject'] = ssubject
                res['subsubsubject'] =  sssubject
                print(f"\t\t\tScraping {i + 1} paper: {res['title']}")
                if len(df) >= 100 and self.page_limit: # upper limit 100 is met
                    break
                df = df.append(res, ignore_index = True)
            except Exception as e:
                traceback.print_exc()
                print("\033[0;36;39mTime to wait for unblocking from the web...\033[0m\n")
                time.sleep(20) # if we are blocked, then, sleep, still can't work
                #print("Can't find this paper!")

        return df


# class to scrape each author's(first author of paper) information
class AuthorsScraper(object):
    """Define Authors's Scraper
    The logic is, we find each other's name and find the link and search it
    """
    def __init__(self, all_author_links, limit = 20,
                 page_limit = False):
        """
        Args :
            --all_author_links: all authors' links then we can use this to find
                each author's papers
            --limit: each author's upper limit
            --page_limit: default is False
        """
        self.all_author_links = all_author_links
        self.limit = limit
        self.upper_limit = 100 # if upper limit is met, we break out from loop
        self.page_limit = page_limit

    def scrape(self, df):
        """This function is used to scrape each author's information, we
        also scrape each author's paper's title and abstract
        # one more logic, if we want to skip to other page(next page)
        # we can change link like this:
        # https://arxiv.org/search/?searchtype=author&query=Jain%2C+S&start=100
        # add &start=100
        """
        flag = False # used to set to True if page_limit and 100 pages are scraped
        for name, link in self.all_author_links.items():
            count = 0
            print('\tScraping author ' + name + ' : ')
            bs = getPage(link)
            page_number = 0
            upper = 0
            while upper < self.upper_limit:
                # get each page
                try:
                    ol = bs.find('ol', {'class' : 'breathe-horizontal'})
                    lis = ol.find_all('li', class_ = 'arxiv-result')
                    length = len(lis)
                    for i in range(length):
                        li_node = lis[i]
                        try:
                            title = li_node.find('p', class_ = 'title is-5 mathjax').text
                            title = title.strip().lstrip('"').rstrip('"').strip()
                            authors = li_node.find('p', class_ = 'authors').text
                            print(f'\t\tScraping {upper + 1} paper --> ')
                            print(f'\t\t\t{title}')
                            if authors.count(name):
                                count += 1
                                print(f'\t\t\t\033[0;36;42mThis paper belongs to {name}.\033[0m')
                                abstract = li_node.find('p', class_ = 'abstract mathjax').\
                                    find('span', {'style' : 'display: none;'}, class_ = 'abstract-full has-text-grey-dark mathjax')
                                abstract = abstract.text.strip().lstrip('"').rstrip('"').strip()
                                res = {'name' : name, 'title' : title, 'abstract' : abstract}
                                df = df.append(res, ignore_index = True)
                                if len(df) >= 100 and self.page_limit: # only consider paper's belong to authors
                                    print('Upper limit 100 pages are scraped!')
                                    flag = True
                                    break

                            upper += 1

                            if upper >= self.upper_limit:
                                print(f'\tBeyond upper limit of searching {upper}.')
                                break

                        except Exception as e:
                            print(e)
                            pass

                    # next page
                    page_number += 1
                    try:
                        bs = BeautifulSoup(urlopen(link + '&start=' + str(page_number * 50)), 'lxml')
                        _ = bs.find('ol', {'class' : 'breathe-horizontal'}).find_all('li', class_ = 'arxiv-result') # to throw exception
                    except:
                        print(f'\tSearching {name} to the end!')
                        break

                except Exception as e:
                    print(e)
                    break

                if flag: # break if upper limit 100 is met
                    break

            if flag:
                break

        return df


# unit test
if __name__ == '__main__':
    import pandas as pd
    all_author_links = {'Sam L. Polk':
                            'https://arxiv.org//search/cs?searchtype=author&query=Polk%2C+S+L',
                        'Dena Bazazian':
                            'https://arxiv.org//search/cs?searchtype=author&query=Bazazian%2C+D',
                        'Sidi Yang':
                            'https://arxiv.org//search/cs?searchtype=author&query=Yang%2C+S'}
    authorscraper = AuthorsScraper(#all_author_links = {'Sam L. Polk':
                                   #'https://arxiv.org//search/cs?searchtype=author&query=Polk%2C+S+L'},
                                  all_author_links)

    df = pd.DataFrame({'name': [], 'title': [], 'abstract': []})
    df = authorscraper.scrape(df)
    print(df)

    # scraper = LinkScraper(subject = 'Computer Science',
    #                       ssubject = 'Computing Research Repository',
    #                       sssubject = 'Computer Vision and Pattern Recognition')
    # scraper.scrape_main_page()
    # print_big_dict(scraper.big_dict, 0)
    # links = scraper.scrape_specific_page(link = 'https://arxiv.org/list/physics.ao-ph/recent')
    # links = scraper.scrape_specific_page(link = 'https://arxiv.org/list/cs.CV/recent')
    # all_links = scraper.scrape_paper_links()
    # print_big_dict(all_links, 0)
    # links = all_links['computer science']['computing research repository']['computer vision and pattern recognition']
    # info_scrape = InfoScraper(links = links)
    # info_scrape.scrape_info()