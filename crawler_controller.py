# -*- coding: utf-8 -*- 

import pandas as pd
import os, sys


df = pd.read_csv('./datas/categories.csv', dtype ='str')

mid_title = df.loc[40,'mid_title']
mid_code = df.loc[40,'mid_code']

page = sys.argv[1] # python mss_crawl_controller.py 3 => 3

command = "cd musinsa/ && scrapy crawl MusinsaItem -o ../datas/mss{}_page{}.csv -a midcode={} -a page={}".format(mid_code, page, mid_code, page)

os.system(command)

dvdr = '*'*30
print(dvdr , "> finished : {} page={}".format(mid_title,page))
