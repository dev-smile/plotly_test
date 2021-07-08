from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import json
import xmltodict
import plotly.graph_objects as go

def cntlvssl() -> list:
    url = 'http://apis.data.go.kr/1192000/CntlVssl2/Info'
    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey'): 'Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3+6o3M4O1nW6YMdRw==', # 인증키
            quote_plus('pageNo'): '1', # 페이지 번호
            quote_plus('numOfRows'): '50', # 한 페이지 결과 수(최대 50)
            quote_plus('prtAgCd'): '030', # 항만청코드(인천항 030)
            quote_plus('sde'): '20210708', # 검색 시작일
            quote_plus('ede'): '20210708', # 검색 종료일
            quote_plus('clsgn'): '' # 호출부호
        }
    )

    req = urlopen(url + queryParams)
    res = req.read().decode('utf8')
    dict_type = xmltodict.parse(res)
    json_type = json.dumps(dict_type)
    dict2_type = json.loads(json_type)

    value = []
    for i in range(5):
        value.append([])
    clsgn = []

    i = 1
    for item in dict2_type["response"]["body"]["items"]["item"]:
        try :
            if item["details"]["detail"][0]["cntrlNm"] == '입항':
                value[0].append(str(i))
                value[1].append(item["vsslNm"])
                value[2].append(item["vsslNltyNm"])
                value[3].append(item["clsgn"])
                clsgn.append(item["clsgn"])
                try:
                    value[4].append(item["details"]["detail"][0]["cntrlOpertDt"])
                except:
                    value[4].append(item["details"]["detail"]["cntrlOpertDt"])
                i += 1
                if i > 10 : break
        except:
            if item["details"]["detail"]["cntrlNm"] == '입항':
                value[0].append(str(i))
                value[1].append(item["vsslNm"])
                value[2].append(item["vsslNltyNm"])
                value[3].append(item["clsgn"])
                clsgn.append(item["clsgn"])
                try:
                    value[4].append(item["details"]["detail"][0]["cntrlOpertDt"])
                except:
                    value[4].append(item["details"]["detail"]["cntrlOpertDt"])
                i += 1
                if i > 10 : break

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=['No', 'Vessel', '선박국가', '콜사인', '기항지입항일시']),
                cells=dict(values=value)
            )
        ]
    )

    fig.show()

    return clsgn

def cargfrghtout(clsgn):
    url = 'http://apis.data.go.kr/1192000/CargFrghtOut2/Info'
    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey'): 'Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3+6o3M4O1nW6YMdRw==', # 인증키
            quote_plus('pageNo'): '1', # 페이지 번호
            quote_plus('numOfRows'): '10', # 한 페이지 결과 수(최대 50)
            quote_plus('prtAgCd'): '030', # 항만청코드(인천항 030)
            quote_plus('etryptYear'): '2021', # 입항연도
            quote_plus('etryptCo'): '001', # 입항횟수
            quote_plus('clsgn'): clsgn # 호출부호
        }
    )

    req = urlopen(url + queryParams)
    res = req.read().decode('utf8')
    dict_type = xmltodict.parse(res)
    json_type = json.dumps(dict_type)
    dict2_type = json.loads(json_type)

    if dict2_type["response"]["body"]["items"] == None :
        url = 'http://apis.data.go.kr/1192000/CargFrghtIn2/Info'
        queryParams = '?' + urlencode(
            {
                quote_plus(
                    'ServiceKey'): 'Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3+6o3M4O1nW6YMdRw==',
                # 인증키
                quote_plus('pageNo'): '1',  # 페이지 번호
                quote_plus('numOfRows'): '10',  # 한 페이지 결과 수(최대 50)
                quote_plus('prtAgCd'): '030',  # 항만청코드(인천항 030)
                quote_plus('etryptYear'): '2021',  # 입항연도
                quote_plus('etryptCo'): '001',  # 입항횟수
                quote_plus('clsgn'): clsgn  # 호출부호
            }
        )

        req = urlopen(url + queryParams)
        res = req.read().decode('utf8')
        dict_type = xmltodict.parse(res)
        json_type = json.dumps(dict_type)
        dict2_type = json.loads(json_type)

        print("Vessel : " + dict2_type["response"]["body"]["items"]["item"]["vsslNm"])
        print("선박종류명 : " + dict2_type["response"]["body"]["items"]["item"]["vsslKndNm"])
        print("화물품목한글명 : " + dict2_type["response"]["body"]["items"]["item"]["frghtPrdlstKorNm"])

    else:
        print("Vessel : " + dict2_type["response"]["body"]["items"]["item"]["vsslNm"])
        print("선박종류명 : " + dict2_type["response"]["body"]["items"]["item"]["vsslKndNm"])
        print("화물품목한글명 : " + dict2_type["response"]["body"]["items"]["item"]["frghtPrdlstKorNm"])

cls = cntlvssl()
i = input("검색할 Vessel의 No를 입력하세요. : ")
cargfrghtout(cls[int(i)-1])