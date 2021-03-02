# -*- coding: utf-8 -*- 


import requests, re, os
import pandas as pd
from bs4 import BeautifulSoup


# category page crawling이 안돼서 rank page에서 접속
rank_url = 'https://search.musinsa.com/ranking/best?period=now&mainCategory=001'

req = requests.get(rank_url)
document = BeautifulSoup(req.content, "html.parser")

# 메인 카테고리 수집
selector = "#goodsRankForm > div.clear > div:nth-child(16) > dl > dd > ul > li > a:nth-child(1)"
elements = document.select(selector)

title = [element.get_text() for element in elements]
ls = [re.search(('\d+'),element['href']).group() for element in elements]
code_list = {"main_title": title, "main_code" : ls}
main_code_df = pd.DataFrame(code_list)


# 미들 카테고리 (중분류) 수집
middle_code_df = pd.DataFrame(columns=['mid_title','mid_code','main_code'])

def category_crawler(sector_code='001'):
    global middle_code_df
    rank_url = 'https://search.musinsa.com/ranking/best?period=now&mainCategory={}'.format(sector_code)
    
    req = requests.get(rank_url)
    dom = BeautifulSoup(req.content, "html.parser")
    
    selector = '#goodsRankForm > div.clear > div:nth-child(17) > dl > dd > ul > li > a'
    mid_sec = dom.select(selector)
    
    sector_title = [element.get_text() for element in mid_sec]
    mid_code = [re.search(('\d+'),element['href']).group() for element in mid_sec]
    main_code = [sector_code] * len(mid_code)
    
    code_list = {"mid_title": sector_title, "mid_code" : mid_code, "main_code": main_code}
    code_list_tmp = pd.DataFrame(code_list)
    
    middle_code_df = middle_code_df.append(code_list_tmp)
    print(sector_code, middle_code_df.tail(1))

    
# 메인 카테고리로 중분류 크롤링 : [주의] 종종 수집이 안되므로 꼭 확인 바람!!
for code in main_code_df.main_code.to_list():
    category_crawler(code)
    
    
# 생성 된 미들 카테고리에 메인 카테고리 이름 넣기
middle_code_df.reset_index(drop=True, inplace=True)
category_df = middle_code_df.join(main_code_df.set_index('main_code'), on='main_code')

# csv로 저장
os.system("mkdir datas")
category_df.to_csv('./datas/categories.csv', index=False, encoding='UTF-8', sep=',' )
