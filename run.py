# -*- coding: utf-8 -*- 

import pandas as pd
import os, sys, time
from category import CategoryCrawler


def start_crawl(main_code='001'):
    cgc = CategoryCrawler()
    category_df = cgc.get_mid_category(main_code)
    
    while True:
        check = input('Need parsing again? (y/n): ')
        if check == 'n':
            break
        else:
            cgc.update_mid_category()
            category_df = cgc.get_mid_category()
            break

    target_df = category_df[category_df['main_code'] == main_code][['mid_title','mid_code']]
    print(target_df)
    
    while True:
        midcode = input('Input start midcode : ')
    
        try:
            target_df = target_df.iloc[target_df[target_df['mid_code'] == midcode].index[0]:]
            break;
        except:
            print(midcode + 'is not in target_df')
   
    target_pages = cgc.parse_page_count(midcode)
    print('target pages : ', target_pages)
    
    while True:
        start_page = input('Input start page : ')
        
        if int(start_page) <= int(target_pages):
            break;
            
    
    for _, mid_title, mid_code in target_df.itertuples():
        for page in range(int(start_page),int(target_pages)+1):
            
            command = f"cd musinsa/ && scrapy crawl Musinsa -a midcode={mid_code} -a page={page}"
            os.system(command)

            dvdr = '*'*40
            print(dvdr , f">> Crawl Finished : {mid_title} page={page}", sep='\n')
            
            time.sleep(3)
