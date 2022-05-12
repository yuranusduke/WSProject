# -*- coding: utf-8 -*-
"""
This file is built to let you run our scrapy program in the command easily

Created by Kunhong Yu(444447)
Date: 2022/05/01
"""
import scrapy
from scrapy.exceptions import CloseSpider
import sys
sys.path.append('../../../') # set path back

from datetime import datetime
from sscrapy.config import Config
from sscrapy.main import mainScrapy
import time

opt_scrapy = Config()

class CommandSpider(scrapy.Spider):
    name = 'commandspider'

    string = '\n' + '*' * 20 + str(datetime.now()) + '*' * 20 + '\n'
    print('Parameters set: ')
    # opt_scrapy.set_kwargs(**kwargs)
    string += opt_scrapy.print_kwargs()
    s = time.time()
    mainScrapy(opt_scrapy)  # just run it!
    e = time.time()
    print('Scraping and plotting approximately elapsed time : {:.2f}s.'.format(e - s))
    string += '*' * 50 + '\n'
    string += 'Elapsed time : ' + str(e - s) + 's.\n'

    with open('../../../records/scrapy_records.txt', 'a+') as f:
        f.write(string)
        f.flush()

    exit(0)