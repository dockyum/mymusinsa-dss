# -*- coding: utf-8 -*- 

import pandas as pd
import os, sys, time
from category import CategoryCrawler


def start_crawl(main_code='001', update_category=False):
    cgc = CategoryCrawler()
    category_df = cgc.get_mid_category(main_code)
    
    if update_category:
        cgc.update_mid_category()
        category_df = cgc.get_mid_category()

    target_df = category_df[category_df['main_code'] == main_code][['mid_title','mid_code']]
    
    for _, mid_title, mid_code in target_df.itertuples():
        target_pages = cgc.parse_page_count(mid_code)
        
        for page in range(int(target_pages)):
            command = f"cd musinsa/ && scrapy crawl Musinsa -a midcode={mid_code} -a page={page+1}"
            os.system(command)

            dvdr = '*'*40
            print(dvdr , f">> Crawl Finished : {mid_title} page={page}", sep='\n')
            
            time.sleep(10)
