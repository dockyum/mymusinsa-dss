# My Musinsa
![Screen Shot 2021-03-03 at 2 15 48 PM](https://user-images.githubusercontent.com/73205057/109778393-1c58c000-7c48-11eb-92c7-315f022a9802.png)
- 기간 : 2021. 02. 22. -  2021. 03. 19.
- [김도겸](https://github.com/dockyum) / item crawling, crawling control, flask
- [장혜임](https://github.com/mieyhgnaj) / size crawling, README
- [👉🏻 발표자료](https://docs.google.com/presentation/d/1GLuuufka8ygB66CV1-vV9kHLrMHbu37cH33GUwRJwnM/edit?usp=sharing)

</br>

## 프로젝트 소개
<img src="https://user-images.githubusercontent.com/73205057/112718921-5eb8a880-8f39-11eb-811d-7e34cee0663c.png"  width="100" height="100"> &ensp; <img src="https://user-images.githubusercontent.com/73205057/112719124-793f5180-8f3a-11eb-8467-88e15e3faaf1.png"  width="100" height="100"> &ensp; <img src="https://user-images.githubusercontent.com/73205057/112719273-7e50d080-8f3b-11eb-8892-0797be96dd16.png"  width="100" height="100"> &ensp; <img src="https://user-images.githubusercontent.com/73205057/112719311-afc99c00-8f3b-11eb-9e7e-cf7c3888fd5c.png"  width="100" height="100"> &ensp; <img src="https://user-images.githubusercontent.com/73205057/112719292-96285480-8f3b-11eb-8310-61ebd3178aea.png"  width="100" height="100">

> 👏🏻 소유하고 있는 옷의  사이즈와 판매 중인 옷의 사이즈를 비교하여  
> &emsp; 나에게 딱 맞는 핏의 옷을 찾는다.
### 목표
무신사 스토어 상품의 데이터를 크롤링하여 유저가 제공한 사이즈와 유사한 상품을 추천한다.

</br>

## 사이트 소개
무신사 스토어(MUSINSA STORE)
- 메인 페이지 url

	> https://<span></span>store.musinsa.com/app/
- 전체 url

	> https://<span></span>search.musinsa.com/category/{ *중분류 번호* }?device=&d_cat_cd=001001&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={ *페이지 번호* }&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q=
- 제품 상세 페이지 url

	> https://<span></span>store.musinsa.com/app/goods/{ *제품 번호* }

</br>

## 프로젝트 결과
### __step 1__    
카테고리에 해당하는 사이즈 정보를 입력받아 전달    
⇒ javascript 활용   

<img src="https://user-images.githubusercontent.com/73205057/112719683-6f6b1d80-8f3d-11eb-87b3-bba1794c3268.GIF"  width="70%">    

### __step 2__    
MySQL 검색 후 결과 리스트 제공   

<img src="https://user-images.githubusercontent.com/73205057/112719979-303dcc00-8f3f-11eb-8bf8-b8e383f75158.gif"  width="70%">

</br>

## 시스템 구조
<img src="https://user-images.githubusercontent.com/73205057/118106221-55679a80-b418-11eb-900d-1519e25d9dbd.png"  width="85%">

</br>

## 프로젝트 진행 과정
<img src="https://user-images.githubusercontent.com/73205057/112720209-59129100-8f40-11eb-9306-74c0fd76d681.png"  width="85%">

</br>

## 01 Crawling
<img src="https://user-images.githubusercontent.com/73205057/112720238-79425000-8f40-11eb-801b-5f077f15ede4.png"  width="85%">    

### 1. 목표 크롤링 페이지: 20만 개    
&emsp; </br>
&emsp; : 서버 1개로 크롤링하기엔 많은 양    
&emsp; </br>
&emsp; => Github <-> AWS instance    

</br>
</br>

<img src="https://user-images.githubusercontent.com/73205057/118107376-a330d280-b419-11eb-9047-0d453a8b0d1f.png"  width="85%">

### 2. 복잡한 size 데이터 크롤링
size title, number가 다양함.

&emsp; </br>
&emsp; : scrapy가 느려짐
</br>
&emsp; => scrapy 2개 사용: 'musinsa', 'size'

</br>
</br>

### 3. 서버 부하 => scrapy setting 조절
```
'CONCURRENT_REQUESTS': 12
# 'CONCURRENT_REQUESTS': 16
'AUTOTHROTTLE_ENABLED': True
# 'AUTOTHROTTLE_ENABLED': False
```

</br>

### 4. Crawling 수행시 나타난 특징적 에러
1. Index out of range    
종종 'User-Agent'가 모바일로 설정되어 response가 m.store.musinsa.com으로 돌아와서 xpath가 틀리다고 나옴    
⇒ settings.py 수정  
```
RANDOMUSERAGENT_RANDOM_UA_TYPE = {
		'hardware_types': 'COMPUTER',
		'popularity': 'POPULAR'
}
```
2. Took longer than 180.0 seconds    
서버에서 응답을 일부러 늦춤 (크롤링 대비)    

</br>

### 5. scrapy response 속도 체험...
__⋇⋇ gif 파일입니다..__    
![속도체험](https://user-images.githubusercontent.com/73205057/112774260-12be4e80-9074-11eb-9471-d5e9d8ae09fe.gif)

</br>

## 02 MySQL 저장
두 개의 테이블 (item, size)    
: size 데이터가 복잡하여 item과 분리해 별도의 table을 만듦    
```
from sqlalchemy import *
import pandas as pd


engine = create_engine("mysql://root:<pswd>@<ip>/mymusinsa?charset=utf8")

class MusinsaPipeline():
    def process_item(self, item, spider):
        df = pd.DataFrame([item])
        df.to_sql('item', con=engine, if_exists='append', index=False)
        engine.execute("SELECT * FROM item").fetchall()
        return item
```

</br>

### 1. size table
제품마다 S, M, L, ... 등의 사이즈 분류가 유동적    
<img src="https://user-images.githubusercontent.com/73205057/118106400-8942c000-b418-11eb-88b0-4124f64f5dfd.png"  width="85%">    
=> 일반적인 컬럼명으로 데이터 구조화    
=> 했지만... 후에 문제 발생..

</br>

## 03 Web Service
<img src="https://user-images.githubusercontent.com/73205057/112721025-0b4c5780-8f45-11eb-935a-626aea7d33ae.gif"  width="70%">
Top / Outer / Pants / Onepiece / Skirt
</br>
: 다섯가지 카테고리로 구별    

</br>
</br>

### 1. javascript
```
function Top() {
            var pic = "https://image.musinsa.com/images/size_type/detail_img/2019070114282500000014799.png"
            document.getElementById('GuideImg').src = pic;
            document.getElementById('GuideImg').style.display = 'block';
            maincode = '001'
        }
```
```
var url = "/getdatas?maincode=" + maincode + "&v1=" + vl1 + "&v2=" + vl2 + "&v3=" + vl3 + "&v4=" + vl4 + "&v5=" + vl5;
```

</br>

### 2. and, or 쿼리...
```
if maincode in ['001', '002', '020']:
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.A_0 == size_values["v1"], Size.A_1 == size_values["v2"], Size.A_2 == size_values["v3"], Size.A_3 == size_values["v4"])).limit(10)
        rs = [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.B_0 == size_values["v1"], Size.B_1 == size_values["v2"], Size.B_2 == size_values["v3"], Size.B_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.C_0 == size_values["v1"], Size.C_1 == size_values["v2"], Size.C_2 == size_values["v3"], Size.C_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.D_0 == size_values["v1"], Size.D_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.E_0 == size_values["v1"], Size.E_1 == size_values["v2"], Size.E_2 == size_values["v3"], Size.E_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.F_0 == size_values["v1"], Size.F_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.G_0 == size_values["v1"], Size.G_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
    elif maincode == '003':
        query_request = Size.query.filter(Size.main_code == maincode).filter(Size.A_0.in_(size_values["v1"])).filter(Size.A_1.in_(size_values["v2"])).filter(Size.A_2.in_(size_values["v3"])).filter(Size.A_3.in_(size_values["v4"])).filter(Size.A_4.in_(size_values["v5"])).limit(5)
        rs = [result.item_id for result in query_request]
    elif maincode == '022':
        query_request = Size.query.filter(Size.main_code == maincode).filter(Size.A_0.in_(size_values["v1"])).filter(Size.A_1.in_(size_values["v2"])).filter(Size.A_2.in_(size_values["v3"])).limit(5)
        rs = [result.item_id for result in query_request]
```

</br>

## 프로젝트 회고
- 옷의 색상 데이터의 경우 selenium을 통한 수집이 필요 했으나 selenium을 동작시켜 확인해보니 필요한 컴퓨팅 자원이 컸기에 수집하지 않기로 결정. 
- 프로젝트 초기에 전체 데이터 크롤링 시간을 예측하여 전체 프로젝트 스케쥴을 세웠는데, 생각보다 크롤링이 오래걸려 후반부 웹서비스 작업을 상대적으로 못하였다. \
  어떤 일이 생길지 모르니 스케쥴 계획은 빡빡하게 세우는 게 필요할 듯.
- 크롤링 속도가 낮아진다면 크롤러(scrapy)를 좀 더 사람처럼 세팅하고 해야겠다.
- 무신사 스토어는 고객이 편리하게 쇼핑을 할 수 있도록 다양한 정보를 제공하고 있지만 \
  크롤링하는 입장에서 html 구조의 일관성이 살짝 부족했다.
- SQL이 서비스의 데이터 흐름을 잘 반영하는 것만으로 서비스의 속도가 달라질 수 있을것 같다
- git은 어렵다.

</br>

## Reference
무신사닷컴(www.musinsa.com)    
Icons made by <a href="https://www.flaticon.com/authors/ddara">dDara</a>, <a href="https://www.freepik.com">Freepik</a>, <a href="https://www.flaticon.com/authors/iconixar" >iconixar</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
