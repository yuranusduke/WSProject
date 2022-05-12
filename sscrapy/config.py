# -*- coding: utf-8 -*-
"""
This file contains sscrapy configurations in this project

Created by Kunhong Yu(444447)
Date: 2022/04/26
"""
class Config(object):
    """
    Args :
        --subject: main page subject, default is 'Computer Science', str or list
        --ssubject: sub-subject, default is 'Computing Research Repository', str or list
        --sssubject: sub-sub-subject, default is 'Computer Vision and Pattern Recognition', str or list
        --limit: number of papers to extract, default is 50
        --page_limit: default is False, setting True will end the program when the number of scraped page is 100
        --analyse: True for analysis and False for not analysis, default is True
        --scrape_each_author: if True, scrape all subject's information regardless of subject, ssubject and
                sssubject
        --crawl: False for not crawling
    """
    subject = ['Computer Science', 'Physics', 'Mathematics']
    ssubject = ['Computing Research Repository', 'Physics', 'Mathematics']
    sssubject = ['Computer Vision and Pattern Recognition', 'Applied Physics',
                 ]
    limit = 26
    page_limit = True
    analyse = False
    scrape_each_author = False
    crawl = True

    def print_kwargs(self):
        """print whole parameters
        return :
            --string
        """
        string = ''
        for k, _ in self.__class__.__dict__.items():
            if not k.startswith('__'):
                line = str(k) + '...' + str(getattr(self, k)) + '\n'
                print(line.rstrip('\n'))
                string += line

        return string

    def set_kwargs(self, **kwargs):
        """Set parameters"""
        for k, v in kwargs.items():
            if not hasattr(self, k):
                print(k + ' does not exist, will be added!')

            setattr(self, k, v)

