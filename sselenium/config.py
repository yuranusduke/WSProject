# -*- coding: utf-8 -*-
"""
This file contains sselenium configurations in this project

Created by Ludi Feng
Date: 2022/05/12
"""


class Config(object):
    """
    Args :
        --subjects: main page subject
        --limit: number of papers to extract, default is 50
        --analyse: True for analysis and False for not analysis, default is True
    """
    subject = ['Computer Science', 'Physics', 'Mathematics']
    ssubject = ['Computing Research Repository', 'Physics', 'Mathematics']
    sssubject = ['Computer Vision and Pattern Recognition',
                 'functional analysis']
    page_limit = True
    limit = 120
    analyse = False
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
