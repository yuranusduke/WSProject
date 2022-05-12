# -*- coding: utf-8 -*-
"""
In this file, we try to scrape the main and get all links of
all papers' pages like the BeautifulSoup one

Created by Kunhong Yu
Date: 2022/04/23
"""
import scrapy
from sscrapy.utils.other_utils import *
from scrapy.crawler import CrawlerProcess
import pandas as pd
import traceback
from twisted.internet import reactor, defer
import itertools

class InfoItem(scrapy.Item):
    """Define Info class for each paper"""
    title = scrapy.Field()
    authors = scrapy.Field()
    first_author_link = scrapy.Field()
    abstract = scrapy.Field()
    comment = scrapy.Field()

class AuthorItem(scrapy.Item):
    """Define author item"""
    name = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()


# 1. Main page spider
# class MainPageSpider(scrapy.Spider):
#     name = 'MainPage'
#
#     def start_requests(self):
#         urls = ["https://arxiv.org/"]
#         return [scrapy.Request(url = url, callback = self.parse) for url in urls]
#
#     def parse(self, response): # the structure is the same as beautiful soup
#         selection = response.css('h2')
#         big_dict = {}
#         for s in selection[1 : -1]:
#             subject = s.xpath('.//text()').extract()[0]
#             print(f'{subject} : ')
#             sub_dict = {}
#             s_selection = response.xpath("//h2[text()=" + "'" + subject + "'" + "]/following-sibling::ul[1]/li")
#             for ss in s_selection:
#                 sub_sub_dict = {}
#                 subsubject = ss.xpath('./a[1]/text()').extract()[0]
#                 print(f'\t{subsubject} : ')
#                 ss_selection = ss.xpath('./br[1]/following-sibling::a')
#
#                 for sss in ss_selection:
#                     subsubsubject = sss.xpath('./text()').extract()[0]
#                     if subsubsubject.count('detailed description'):
#                         continue
#                     print(f'\t\t{subsubsubject} : ', end = '')
#                     url = 'https://arxiv.org' + sss.xpath('./@href').extract()[0]
#                     print(f'{url}')
#                     sub_sub_dict[subsubsubject.lower()] = url
#
#                 sub_dict[subsubject.lower()] = sub_sub_dict
#
#             big_dict[subject.lower()] = sub_dict
#
#         return big_dict
# Due to technique problem, we can not first scrape links and pass
# links to another CrawlerProcess, therefore, we still use BeautifulSoup
# to scrape main page

class MainPageScraper(object):
    """Define main page link scraper class
    Copied from soup subproject
    """
    def __init__(self):
<<<<<<< HEAD
        self.base_url = 'https://arxiv.org/'
        #self.base_url = 'http://xxx.itp.ac.cn/'
=======
        #self.base_url = 'https://arxiv.org/'
        self.base_url = 'http://xxx.itp.ac.cn/'
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8

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
                if subject.text.count('About arXiv'):
                    continue
                print(f'{subject.text} : ')
                ul = subject.find_next('ul')
                lis = ul.find_all('li')
                ss_dict = {}
                for li in lis: # sub-subject
                    ssubject = li.find('a') # get the name of the subsubject
                    ss_text = ssubject.text.lower()
                    print(f'\t{ss_text} : ')
                    # we aim to find sub-sub-subject's link

                    sss_dict = {}
                    try:
                        sssubject = li.find('br').next_siblings
                        sssubject = [x for x in sssubject if x.find('a') != -1] # find <a>
                        for sss in sssubject: # sub-sub-subject
                            sss_text = sss.text.lower()
                            if sss_text.count('detailed description'): # bug here
                                continue
                            print(f'\t\t{sss_text} : ', end = '')
                            url = self.base_url + sss.attrs['href']
                            print(f'{url}')
                            sss_dict[sss_text] = url
                    except:
                        pass#print(ss_text)

                    ss_dict[ss_text] = sss_dict

                big_dict[subject.text.lower()] = ss_dict

            self.big_dict = big_dict

        except Exception as e:
            traceback.print_exc()

        return self.big_dict

# 2. Now we need to scrape each link's papers
class PaperSpider(scrapy.Spider):
    name = 'Papers'

    def __init__(self,
                 start_url,
                 subject,
                 ssubject,
                 sssubject,
                 dict_,
                 df,
                 author_links,
                 df_authors = None,
                 author_dict = None,
                 page_limit = False,
                 limit = 50):
        """
        Args :
            --start_url: starting url
            --limit: upper limit of scrape, default is 50
            --subject: main subject
            --ssubject: subsubject
            --sssubject: subsubsubject
            --dict_: big dict to store information
            --author_links: author's links
            --df: pandas DataFrame instance to store information
            --df_authors/author_dict: defaults are None
            --page_limit: default is False, setting True will end the program when the number of scraped page is 100
        """
        super(PaperSpider, self).__init__()
        self.start_urls = [start_url]
<<<<<<< HEAD
        self.base_url = 'https://arxiv.org'
        #self.base_url = 'http://xxx.itp.ac.cn'
=======
        #self.base_url = 'https://arxiv.org'
        self.base_url = 'http://xxx.itp.ac.cn'
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8
        self.allowed_domains = [start_url.lstrip(self.base_url)]
        self.limit = limit
        self.count = 0
        self.s = subject
        self.ss = ssubject
        self.sss = sssubject
        self.result = dict_
        self.df = df
        self.author_links = author_links
        self.page_limit = page_limit

        self.upper_flag1 = False # if upper limit for PAPERS 100 is achieved, break the program
        self.upper_flag2 = False # if upper limit for EACH AUTHOR's PAPERS 100 is achieved, break the program

        self.df_authors = df_authors
        self.author_dict = author_dict
        self.flag = True

        self.author_count = {}

    def parse(self, response):
        xpath = '//dl'
        selections = response.xpath(xpath)

        # for each page
        for s in selections: # for each date
            s_selections = s.xpath('.//dt')
            for ss in s_selections:
                # find span with class = 'list-identifier'
                node = ss.xpath(".//span[@class = 'list-identifier']")
                # find link
                link = self.base_url + node.xpath('.//a[1]/@href').extract()[0]

                # for each paper link, we scrape its information
                # https://stackoverflow.com/questions/53278942/how-to-send-another-request-and-get-result-in-scrapy-parse-function
                if self.count >= self.limit:
                    print(f'\t\t\t{self.sss} Upper limit number of papers achieved!')
                    self.flag = False
                    break

                if self.upper_flag1:
                    print(f'\t\t\t{self.sss} Upper limit number of papers 100 achieved!')
                    break

                try:
                    yield scrapy.Request(link, callback = self.parse_paper,
                                         dont_filter = True) # !!!!
                except:
                    pass

            if not self.flag:
                break

            if self.upper_flag1:
                break

        # next page
        if self.flag:
            if not self.upper_flag1: # go to the next page
                next_path = '//small[1]//b[1]/following-sibling::a[1]/@href'
                get_next = response.xpath(next_path)
                if get_next:
                    yield scrapy.Request(self.base_url + get_next.extract()[0],
                                         callback = self.parse,
                                         dont_filter = True)

    def parse_paper(self, response):
        # 3. Info Spider
        # this is a single page, so we only need to scrapy its information
        # return :
        #   --item containing title, authors_names, first_author_link, abstract, comment
        # 1. get title
        title_xpath = "//h1[@class = 'title mathjax'][1]/text()"
        title = response.xpath(title_xpath).extract()
        title = ''.join(title).strip().lstrip('"').rstrip('"').strip()

        # 2. get authors
        authors_xpath = "//div[@class='authors']//a"
        authors = response.xpath(authors_xpath)
        authors_names = []
        count = 0
        first_author_link = None
        for a in authors:
            name = ''.join(a.xpath('./text()').extract()).strip()
            authors_names.append(name)
            if count == 0:
                first_author_link = a.xpath('./@href').extract()[0]

            count += 1

        authors_names = ', '.join(authors_names)

        # 3. get abstract
        abstract_xpath = "//blockquote[@class='abstract mathjax']/text()"
        abstract = ''.join(response.xpath(abstract_xpath).extract())
        abstract = abstract.strip().lstrip('"').rstrip('"').strip()

        # 4. get comment
        try:  # some comments not exists
            comment_xpath = "//table[@summary = 'Additional metadata']//td[text()='Comments:']"
            comment = response.xpath(comment_xpath)
            if not comment:
                raise MyExpcetion()
            else:
                comment = ''.join(comment.xpath('./following-sibling::td[1]/text()').extract())
                comment = comment.strip().lstrip('"').rstrip('"').strip()

        except MyExpcetion: # comment does not exist
            comment = ""

        if not self.page_limit and self.count >= self.limit: # avoid to be stored
            self.flag = False
            return

        if len(self.df) >= 100 and self.page_limit: # upper limit is met, so return
            self.upper_flag1 = True
            return

        item = InfoItem()
        item['title'] = title
        item['authors'] = authors_names
        item['first_author_link'] = first_author_link
        item['abstract'] = abstract
        item['comment'] = comment
        self.result[self.s][self.ss][self.sss].append(item)
        self.df.loc[len(self.df.index)] = [self.s, self.ss, self.sss, title, authors_names,
                                           abstract, comment]
        self.count += 1
        if not self.page_limit and self.count >= self.limit:
            self.flag = False
            return  # logic here is if we scrape more than limit papers, than there are at least papers to be scraped related to all authors

        if len(self.df) >= 100 and self.page_limit: # upper limit is met, so return
            self.upper_flag1 = True
            return

        first_author = authors_names.split(', ')[0]
        self.author_links[first_author] = first_author_link

        if isinstance(self.df_authors, pd.DataFrame) and not self.upper_flag2: # we need to scrape each author's paper here
            yield scrapy.Request(first_author_link, callback = self.parse_author,
                                 dont_filter = True, cb_kwargs = {'author_name' : first_author})
        else:
            yield item


    # Next, we scrape each author's information
    # Date: 2022/04/25
    # In this class, we tend to use sscrapy to scrape more information about each paper's information.
    # In particular, we scrape how many papers are related to this authors its name and
    # abstract, and we store them in the file folder for each author, so we can analyses
    # what he/she has been doing during the academic career.
    def parse_author(self, response, author_name):
        # what we need lies in <li> with class = 'arxiv-result' and
        # title starts with 'title ' in <p>, authors are in <p> class = 'authors',
        # abstract is in <p> with class = 'abstract mathjax'
        # get name, if name does not lie in the site, we skip
        # we set limit as 1000 for simplicity
        papers_xpaths = "//li[@class='arxiv-result']"
        papers = response.xpath(papers_xpaths)

        for paper in papers:
            title = paper.xpath(".//p[@class='title is-5 mathjax']/text()").extract_first()
            title = title.strip().lstrip('"').rstrip('"').strip()
            cur_name = paper.xpath(".//p[@class='authors']/span/following-sibling::*//text()").extract()
            abstract = paper.xpath(".//p[@class='abstract mathjax']/span[2]//text()").extract_first()
            abstract = abstract.strip().lstrip('"').rstrip('"').strip()

            if author_name not in self.author_count:
                self.author_count[author_name] = 1
            else:
                self.author_count[author_name] += 1

            if author_name not in self.author_dict:
                self.author_dict[author_name] = [(cur_name, title)]
            else:
                self.author_dict[author_name].append((cur_name, title))

            if ''.join(cur_name).strip().count(author_name) == 0:
                continue

            if not self.page_limit and self.author_count[author_name] >= 100:
                print(f'\t\t\t{self.sss} Upper limit 100 for this author is met!')
                self.upper_flag2 = True
                return

            if self.page_limit and len(self.df_authors) >= 100: # return if all papers are scraped
                self.upper_flag2 = True
                break

            node = AuthorItem()
            node['name'] = author_name
            node['title'] = title
            node['abstract'] = abstract
            self.df_authors.loc[len(self.df_authors.index)] = \
                [node['name'], node['title'], node['abstract']]

            if not self.page_limit and self.author_count[author_name] >= 100:
                print(f'\t\t\t{self.sss} Upper limit 100 for this author is met!')
                self.upper_flag2 = True
                return

            if self.page_limit and len(self.df_authors) >= 100: # return if all papers are scraped
                self.upper_flag2 = True
                break

        next_page = response.css('.pagination-next::attr(href)').get()

        if next_page and not self.upper_flag2:
            yield scrapy.Request(url = response.urljoin(next_page), callback = self.parse_author,
                                 dont_filter = True, cb_kwargs = {'author_name' : author_name})


# 4. Combine them together
class ScrapySpider(object):
    """Define whole scrapy spider"""
    def __init__(self,
                 limit = 50,
                 scrape_each_author = False,
                 page_limit = False,
                 subject = ['Computer Science', 'Physics', 'Mathematics'],
                 ssubject = ['Computing Research Repository', 'Physics', 'Mathematics'],
                 sssubject = ['Computer Vision and Pattern Recognition', 'Machine Learning', 'Applied Physics', 'functional analysis']):
        """
        Args :
            --limit: upper limit of scrapy, default is 50
            --page_limit: default is False, setting True will end the program when the number of scraped page is 100
            --scrape_each_author: default is False
            --subject: main subject
            --ssubject: subsubject
            --sssubject: subsubsubject
        """
        self.limit = limit
        self.subject = subject
        self.ssubject = ssubject
        self.sssubject = sssubject
        self.scrape_each_author = scrape_each_author
        self.page_limit = page_limit

        self.subject = [x.lower() for x in self.subject]
        self.ssubject = [x.lower() for x in self.ssubject]
        self.sssubject = [x.lower() for x in self.sssubject]

        self.author_links = {}
        self.df = pd.DataFrame({'subject' : [], 'subsubject' : [], 'subsubsubject' : [],
                                'title': [], 'authors': [], 'abstract': [],
                                'comment': []})

        self.author_dict = None
        self.df_authors = None
        if self.scrape_each_author:
            self.author_dict = {}
            self.df_authors = pd.DataFrame({'name' : [], 'title': [], 'abstract': []})

        self.runner = CrawlerProcess({'LOG_LEVEL': 'WARNING'}) # don't set depth-limit, if set 10, it will scrape most 10 parse functions
        self.result = {}
        for s in self.subject:
            ssubject_dict = {}

            for ss in self.ssubject:
                sssubject_dict = {}

                for sss in self.sssubject:
                    sssubject_dict[sss] = []

                ssubject_dict[ss] = sssubject_dict

            self.result[s] = ssubject_dict

    # https://stackoverflow.com/questions/47427271/scrapy-running-multiple-spiders-from-the-same-python-process-via-cmdline-fails?rq=1
    @defer.inlineCallbacks
    def spider(self):
        # now we combine them to get what we need
        # 1. scrape main page
        print('\033[0;36;40mStarting scraping main page to get link...\033[0m')
        mainpage = MainPageScraper()
        links = mainpage.scrape_main_page()

        #links = {'physics': {'astrophysics': {'astrophysics of galaxies': 'https://arxiv.org/list/astro-ph.GA/recent', 'cosmology and nongalactic astrophysics': 'https://arxiv.org/list/astro-ph.CO/recent', 'earth and planetary astrophysics': 'https://arxiv.org/list/astro-ph.EP/recent', 'high energy astrophysical phenomena': 'https://arxiv.org/list/astro-ph.HE/recent', 'instrumentation and methods for astrophysics': 'https://arxiv.org/list/astro-ph.IM/recent', 'solar and stellar astrophysics': 'https://arxiv.org/list/astro-ph.SR/recent'}, 'condensed matter': {'disordered systems and neural networks': 'https://arxiv.org/list/cond-mat.dis-nn/recent', 'materials science': 'https://arxiv.org/list/cond-mat.mtrl-sci/recent', 'mesoscale and nanoscale physics': 'https://arxiv.org/list/cond-mat.mes-hall/recent', 'other condensed matter': 'https://arxiv.org/list/cond-mat.other/recent', 'quantum gases': 'https://arxiv.org/list/cond-mat.quant-gas/recent', 'soft condensed matter': 'https://arxiv.org/list/cond-mat.soft/recent', 'statistical mechanics': 'https://arxiv.org/list/cond-mat.stat-mech/recent', 'strongly correlated electrons': 'https://arxiv.org/list/cond-mat.str-el/recent', 'superconductivity': 'https://arxiv.org/list/cond-mat.supr-con/recent'}, 'general relativity and quantum cosmology': {}, 'high energy physics - experiment': {}, 'high energy physics - lattice': {}, 'high energy physics - phenomenology': {}, 'high energy physics - theory': {}, 'mathematical physics': {}, 'nonlinear sciences': {'adaptation and self-organizing systems': 'https://arxiv.org/list/nlin.AO/recent', 'cellular automata and lattice gases': 'https://arxiv.org/list/nlin.CG/recent', 'chaotic dynamics': 'https://arxiv.org/list/nlin.CD/recent', 'exactly solvable and integrable systems': 'https://arxiv.org/list/nlin.SI/recent', 'pattern formation and solitons': 'https://arxiv.org/list/nlin.PS/recent'}, 'nuclear experiment': {}, 'nuclear theory': {}, 'physics': {'accelerator physics': 'https://arxiv.org/list/physics.acc-ph/recent', 'applied physics': 'https://arxiv.org/list/physics.app-ph/recent', 'atmospheric and oceanic physics': 'https://arxiv.org/list/physics.ao-ph/recent', 'atomic and molecular clusters': 'https://arxiv.org/list/physics.atm-clus/recent', 'atomic physics': 'https://arxiv.org/list/physics.atom-ph/recent', 'biological physics': 'https://arxiv.org/list/physics.bio-ph/recent', 'chemical physics': 'https://arxiv.org/list/physics.chem-ph/recent', 'classical physics': 'https://arxiv.org/list/physics.class-ph/recent', 'computational physics': 'https://arxiv.org/list/physics.comp-ph/recent', 'data analysis, statistics and probability': 'https://arxiv.org/list/physics.data-an/recent', 'fluid dynamics': 'https://arxiv.org/list/physics.flu-dyn/recent', 'general physics': 'https://arxiv.org/list/physics.gen-ph/recent', 'geophysics': 'https://arxiv.org/list/physics.geo-ph/recent', 'history and philosophy of physics': 'https://arxiv.org/list/physics.hist-ph/recent', 'instrumentation and detectors': 'https://arxiv.org/list/physics.ins-det/recent', 'medical physics': 'https://arxiv.org/list/physics.med-ph/recent', 'optics': 'https://arxiv.org/list/physics.optics/recent', 'physics and society': 'https://arxiv.org/list/physics.soc-ph/recent', 'physics education': 'https://arxiv.org/list/physics.ed-ph/recent', 'plasma physics': 'https://arxiv.org/list/physics.plasm-ph/recent', 'popular physics': 'https://arxiv.org/list/physics.pop-ph/recent', 'space physics': 'https://arxiv.org/list/physics.space-ph/recent'}, 'quantum physics': {}}, 'mathematics': {'mathematics': {'algebraic geometry': 'https://arxiv.org/list/math.AG/recent', 'algebraic topology': 'https://arxiv.org/list/math.AT/recent', 'analysis of pdes': 'https://arxiv.org/list/math.AP/recent', 'category theory': 'https://arxiv.org/list/math.CT/recent', 'classical analysis and odes': 'https://arxiv.org/list/math.CA/recent', 'combinatorics': 'https://arxiv.org/list/math.CO/recent', 'commutative algebra': 'https://arxiv.org/list/math.AC/recent', 'complex variables': 'https://arxiv.org/list/math.CV/recent', 'differential geometry': 'https://arxiv.org/list/math.DG/recent', 'dynamical systems': 'https://arxiv.org/list/math.DS/recent', 'functional analysis': 'https://arxiv.org/list/math.FA/recent', 'general mathematics': 'https://arxiv.org/list/math.GM/recent', 'general topology': 'https://arxiv.org/list/math.GN/recent', 'geometric topology': 'https://arxiv.org/list/math.GT/recent', 'group theory': 'https://arxiv.org/list/math.GR/recent', 'history and overview': 'https://arxiv.org/list/math.HO/recent', 'information theory': 'https://arxiv.org/list/math.IT/recent', 'k-theory and homology': 'https://arxiv.org/list/math.KT/recent', 'logic': 'https://arxiv.org/list/math.LO/recent', 'mathematical physics': 'https://arxiv.org/list/math.MP/recent', 'metric geometry': 'https://arxiv.org/list/math.MG/recent', 'number theory': 'https://arxiv.org/list/math.NT/recent', 'numerical analysis': 'https://arxiv.org/list/math.NA/recent', 'operator algebras': 'https://arxiv.org/list/math.OA/recent', 'optimization and control': 'https://arxiv.org/list/math.OC/recent', 'probability': 'https://arxiv.org/list/math.PR/recent', 'quantum algebra': 'https://arxiv.org/list/math.QA/recent', 'representation theory': 'https://arxiv.org/list/math.RT/recent', 'rings and algebras': 'https://arxiv.org/list/math.RA/recent', 'spectral theory': 'https://arxiv.org/list/math.SP/recent', 'statistics theory': 'https://arxiv.org/list/math.ST/recent', 'symplectic geometry': 'https://arxiv.org/list/math.SG/recent'}}, 'computer science': {'computing research repository': {'artificial intelligence': 'https://arxiv.org/list/cs.AI/recent', 'computation and language': 'https://arxiv.org/list/cs.CL/recent', 'computational complexity': 'https://arxiv.org/list/cs.CC/recent', 'computational engineering, finance, and science': 'https://arxiv.org/list/cs.CE/recent', 'computational geometry': 'https://arxiv.org/list/cs.CG/recent', 'computer science and game theory': 'https://arxiv.org/list/cs.GT/recent', 'computer vision and pattern recognition': 'https://arxiv.org/list/cs.CV/recent', 'computers and society': 'https://arxiv.org/list/cs.CY/recent', 'cryptography and security': 'https://arxiv.org/list/cs.CR/recent', 'data structures and algorithms': 'https://arxiv.org/list/cs.DS/recent', 'databases': 'https://arxiv.org/list/cs.DB/recent', 'digital libraries': 'https://arxiv.org/list/cs.DL/recent', 'discrete mathematics': 'https://arxiv.org/list/cs.DM/recent', 'distributed, parallel, and cluster computing': 'https://arxiv.org/list/cs.DC/recent', 'emerging technologies': 'https://arxiv.org/list/cs.ET/recent', 'formal languages and automata theory': 'https://arxiv.org/list/cs.FL/recent', 'general literature': 'https://arxiv.org/list/cs.GL/recent', 'graphics': 'https://arxiv.org/list/cs.GR/recent', 'hardware architecture': 'https://arxiv.org/list/cs.AR/recent', 'human-computer interaction': 'https://arxiv.org/list/cs.HC/recent', 'information retrieval': 'https://arxiv.org/list/cs.IR/recent', 'information theory': 'https://arxiv.org/list/cs.IT/recent', 'logic in computer science': 'https://arxiv.org/list/cs.LO/recent', 'machine learning': 'https://arxiv.org/list/cs.LG/recent', 'mathematical software': 'https://arxiv.org/list/cs.MS/recent', 'multiagent systems': 'https://arxiv.org/list/cs.MA/recent', 'multimedia': 'https://arxiv.org/list/cs.MM/recent', 'networking and internet architecture': 'https://arxiv.org/list/cs.NI/recent', 'neural and evolutionary computing': 'https://arxiv.org/list/cs.NE/recent', 'numerical analysis': 'https://arxiv.org/list/cs.NA/recent', 'operating systems': 'https://arxiv.org/list/cs.OS/recent', 'other computer science': 'https://arxiv.org/list/cs.OH/recent', 'performance': 'https://arxiv.org/list/cs.PF/recent', 'programming languages': 'https://arxiv.org/list/cs.PL/recent', 'robotics': 'https://arxiv.org/list/cs.RO/recent', 'social and information networks': 'https://arxiv.org/list/cs.SI/recent', 'software engineering': 'https://arxiv.org/list/cs.SE/recent', 'sound': 'https://arxiv.org/list/cs.SD/recent', 'symbolic computation': 'https://arxiv.org/list/cs.SC/recent', 'systems and control': 'https://arxiv.org/list/cs.SY/recent'}}, 'quantitative biology': {'quantitative biology': {'biomolecules': 'https://arxiv.org/list/q-bio.BM/recent', 'cell behavior': 'https://arxiv.org/list/q-bio.CB/recent', 'genomics': 'https://arxiv.org/list/q-bio.GN/recent', 'molecular networks': 'https://arxiv.org/list/q-bio.MN/recent', 'neurons and cognition': 'https://arxiv.org/list/q-bio.NC/recent', 'other quantitative biology': 'https://arxiv.org/list/q-bio.OT/recent', 'populations and evolution': 'https://arxiv.org/list/q-bio.PE/recent', 'quantitative methods': 'https://arxiv.org/list/q-bio.QM/recent', 'subcellular processes': 'https://arxiv.org/list/q-bio.SC/recent', 'tissues and organs': 'https://arxiv.org/list/q-bio.TO/recent'}}, 'quantitative finance': {'quantitative finance': {'computational finance': 'https://arxiv.org/list/q-fin.CP/recent', 'economics': 'https://arxiv.org/list/q-fin.EC/recent', 'general finance': 'https://arxiv.org/list/q-fin.GN/recent', 'mathematical finance': 'https://arxiv.org/list/q-fin.MF/recent', 'portfolio management': 'https://arxiv.org/list/q-fin.PM/recent', 'pricing of securities': 'https://arxiv.org/list/q-fin.PR/recent', 'risk management': 'https://arxiv.org/list/q-fin.RM/recent', 'statistical finance': 'https://arxiv.org/list/q-fin.ST/recent', 'trading and market microstructure': 'https://arxiv.org/list/q-fin.TR/recent'}}, 'statistics': {'statistics': {'applications': 'https://arxiv.org/list/stat.AP/recent', 'computation': 'https://arxiv.org/list/stat.CO/recent', 'machine learning': 'https://arxiv.org/list/stat.ML/recent', 'methodology': 'https://arxiv.org/list/stat.ME/recent', 'other statistics': 'https://arxiv.org/list/stat.OT/recent', 'statistics theory': 'https://arxiv.org/list/stat.TH/recent'}}, 'electrical engineering and systems science': {'electrical engineering and systems science': {'audio and speech processing': 'https://arxiv.org/list/eess.AS/recent', 'image and video processing': 'https://arxiv.org/list/eess.IV/recent', 'signal processing': 'https://arxiv.org/list/eess.SP/recent', 'systems and control': 'https://arxiv.org/list/eess.SY/recent'}}, 'economics': {'economics': {'econometrics': 'https://arxiv.org/list/econ.EM/recent', 'general economics': 'https://arxiv.org/list/econ.GN/recent', 'theoretical economics': 'https://arxiv.org/list/econ.TH/recent'}}}
        print('\033[0;36;40mScraping main page to get link is done!\033[0m')

        # 2. scrape paper's links and information
        print('\033[0;36;40mStarting scraping paper\'s info to get link...\033[0m')
        for s in self.subject:
            if s not in links:
                continue
            s_links = links[s]

            for ss in self.ssubject:
                if ss not in s_links:
                    continue
                ss_links = s_links[ss]
                for sss in self.sssubject:
                    if sss not in ss_links:
                        continue
                    sss_link = ss_links[sss]
                    # scrape now
                    # 2.1 get links for each paper
                    # 2.2 scrape each paper's information
                    yield self.runner.crawl(PaperSpider, subject = s, ssubject = ss,
                                            sssubject = sss, start_url = sss_link,
                                            limit = self.limit, dict_ = self.result,
                                            df = self.df, author_links = self.author_links,
                                            page_limit = self.page_limit,
                                            df_authors = self.df_authors, author_dict = self.author_dict)

        reactor.stop()

        # 3. Save to csv file
        # due to the fact we can not control how many papers are scraped
        # when set page_limit to be True, we truncate them when there are more than 100 papers
        if self.page_limit:
            self.result = dict(itertools.islice(self.result.items(), 100))
            self.author_links = dict(itertools.islice(self.author_links.items(), 100))

        if self.page_limit and len(self.df) > 100:
            self.df = self.df[:100]
        try:
            self.df.to_csv('./sscrapy/data/allinfo.csv', index = False, sep = '#')
        except: # change dir when use this function in the command line
            self.df.to_csv('../../data/allinfo.csv', index = False, sep = '#')
        if self.scrape_each_author:
            if self.page_limit and len(self.df) > 100:
                self.df_authors = self.df_authors[:100]
            try:
                self.df_authors.to_csv('./sscrapy/data/allauthorsinfo.csv', index = False, sep = '#')
            except:  # change dir when use this function in the command line
                self.df_authors.to_csv('../../data/allauthorsinfo.csv', index = False, sep = '#')



# unit test
if __name__ == '__main__':
    # run scrapy inside script
    # get rid of warning message
    # FROM: https://stackoverflow.com/questions/33203620/how-to-turn-off-logging-in-scrapy-python
    # process = CrawlerProcess({'LOG_LEVEL': 'WARNING'})
    # process.crawl(MainPageSpider)
    # process.start()

    pass