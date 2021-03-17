# -*- coding: utf-8 -*- 


import requests, re, os
import pandas as pd
from bs4 import BeautifulSoup


## [TODO] : 카테고리를 크롤링하는 class로서 
## 1. crawling된 mid_category 중 잘못 된 것이 있을 경우 그 부분만 따로 crawling
## 2. csv file을 새로 만들것인지 crawling만 할 것인지 선택하도록,
class CategoryCrawler:
    def __init__(self):
        self.main_code_df = pd.DataFrame(columns=['main_title','main_code'])
        self.middle_code_df = pd.DataFrame(columns=['mid_title','mid_code','main_code'])
        
    def parse_main_category(self):
        try:
            url = 'https://search.musinsa.com/ranking/best?period=now&mainCategory=001'
            req = requests.get(url)
            print('request main : ',req)
        except requests.exceptions.RequestException as e: 
            raise SystemExit(e)

        document = BeautifulSoup(req.content, "html.parser")
        selector = "#goodsRankForm > div.clear > div:nth-child(16) > dl > dd > ul > li > a:nth-child(1)"
        elements = document.select(selector)
        title = [element.get_text() for element in elements]
        ls = [re.search(('\d+'),element['href']).group() for element in elements]
        code_dict = {"main_title": title, "main_code" : ls}
        
        self.main_code_df = pd.DataFrame(code_dict)
        
    def get_main_category(self):
        if self.middle_code_df['mid_title'].size == 0:
            self.parse_main_category()
        return self.main_code_df
        
    def parse_mid_category(self, main_code=None):
        if self.main_code_df['main_title'].size == 0:
            self.parse_main_category()
        if main_code:
            try:
                url = 'https://search.musinsa.com/ranking/best?period=now&age=ALL&mainCategory={}'.format(main_code)
                req = requests.get(url)
                print(f'request {main_code} : ', req)
            except requests.exceptions.RequestException as e: 
                raise SystemExit(e)

            document = BeautifulSoup(req.content, "html.parser")    
            selector = '#goodsRankForm > div.clear > div:nth-child(17) > dl > dd > ul > li > a'
            mid_sec = document.select(selector)
            mid_title = [element.get_text() for element in mid_sec]
            mid_code = [re.search(('\d+'),element['href']).group() for element in mid_sec]
            main_codels = [main_code] * len(mid_code)

            code_dict = {"mid_title": mid_title, "mid_code" : mid_code, "main_code": main_codels}
            code_list_tmp = pd.DataFrame(code_dict)

            self.middle_code_df = self.middle_code_df.append(code_list_tmp)
            print(main_code, self.middle_code_df.tail(1))
            self.middle_code_df.reset_index(drop=True, inplace=True)
            print(f'------------finished parsing for all "{main_code}"-----------')
            
        else:
            for code in self.main_code_df['main_code']:
                try:
                    url = 'https://search.musinsa.com/ranking/best?period=now&age=ALL&mainCategory={}'.format(code)
                    req = requests.get(url)
                    print(f'request {code} : ', req)
                except requests.exceptions.RequestException as e: 
                    raise SystemExit(e)

                document = BeautifulSoup(req.content, "html.parser")    
                selector = '#goodsRankForm > div.clear > div:nth-child(17) > dl > dd > ul > li > a'
                mid_sec = document.select(selector)
                mid_title = [element.get_text() for element in mid_sec]
                mid_code = [re.search(('\d+'),element['href']).group() for element in mid_sec]
                main_codels = [code] * len(mid_code)

                code_dict = {"mid_title": mid_title, "mid_code" : mid_code, "main_code": main_codels}
                code_list_tmp = pd.DataFrame(code_dict)

                self.middle_code_df = self.middle_code_df.append(code_list_tmp)
                print(code, self.middle_code_df.tail(1))
            self.middle_code_df.reset_index(drop=True, inplace=True)
            print('------------finished parsing for all mid_code-----------')

    def get_mid_category(self, main_code=None):
        if self.middle_code_df["mid_title"].size == 0:
            self.parse_mid_category(main_code)
        return self.middle_code_df
            
    def update_mid_category(self):
        if self.middle_code_df["mid_title"].size == 0:
            print('run "parse_mid_category" first')
        else:
            while True:
                category_code = input('check a "Main Code" again(quit: q): ')
                if category_code in self.middle_code_df['main_code'].values:
                    self.middle_code_df.drop(
                        self.middle_code_df[self.middle_code_df['main_code'] == category_code].index, inplace=True)
                    try:
                        url = 'https://search.musinsa.com/ranking/best?period=now&age=ALL&mainCategory={}'.format(category_code)
                        req = requests.get(url)
                        print(f'request {category_code} : ',req)
                    except requests.exceptions.RequestException as e:  
                        raise SystemExit(e)

                    document = BeautifulSoup(req.content, "html.parser")
                    selector = '#goodsRankForm > div.clear > div:nth-child(17) > dl > dd > ul > li > a'
                    mid_sec = document.select(selector)
                    mid_title = [element.get_text() for element in mid_sec]
                    mid_code = [re.search(('\d+'),element['href']).group() for element in mid_sec]
                    main_code = [category_code] * len(mid_code)

                    code_dict = {"mid_title": mid_title, "mid_code" : mid_code, "main_code": main_code}
                    code_list_tmp = pd.DataFrame(code_dict)

                    self.middle_code_df = self.middle_code_df.append(code_list_tmp)
                    print('parse done : ', category_code, self.middle_code_df.tail(1))
                elif category_code == 'q':
                    break
                else:
                    print('invalid code. try again')
                    continue

                update_check = input('Update more ? [y,n]: ')
                if update_check == 'y':
                    continue
                else:
                    print('finished update')
                    break
        
    def parse_page_count(self, mid_code):
        if self.middle_code_df["mid_title"].size == 0:
            print('run "parse_mid_category" first')
        try:
            url = f'https://search.musinsa.com/category/{mid_code}'
            req = requests.get(url)
            print(f'parse page_counts {mid_code} : ', req)
        except requests.exceptions.RequestException as e: 
            raise SystemExit(e)

        document = BeautifulSoup(req.content, "html.parser")
        selector = 'span.totalPagingNum'
        tot_pages = document.select_one(selector).get_text()
        return tot_pages
        
    def save_csv(self):
        middle_code_df = self.middle_code_df.reset_index(drop=True)
        category_df = middle_code_df.join(main_code_df.set_index('main_code'), on='main_code')

        if not os.path.isdir('datas'):
            os.makedirs('datas')
        category_df.to_csv('./datas/categories.csv', index=False, encoding='UTF-8', sep=',' )
