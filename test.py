from pprint import pprint
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import json
import xmltodict

url = 'http://apis.data.go.kr/1192000/VsslEtrynd2/Info'
queryParams = '?' + urlencode(
    {
        quote_plus('ServiceKey'): 'Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3+6o3M4O1nW6YMdRw==', # 인증키
        quote_plus('pageNo'): '1', # 페이지 번호
        quote_plus('numOfRows'): '50', # 한 페이지 결과 수(최대 50)
        quote_plus('prtAgCd'): '030', # 항만청코드(인천항 030)
        quote_plus('sde'): '20210629', # 검색 시작일
        quote_plus('ede'): '20210629', # 검색 종료일
        quote_plus('clsgn'): '' # 호출부호
    }
)

req = urlopen(url + queryParams)
res = req.read().decode('utf8')
dict_type = xmltodict.parse(res)
json_type = json.dumps(dict_type)
dict2_type = json.loads(json_type)
# pprint(dict2_type["response"]["body"]["items"]["item"])
i = 1
for item in dict2_type["response"]["body"]["items"]["item"]:
    print("No : " + str(i))
    print("Vessel : " + item["vsslNm"])
    print("선박국가 : " + item["vsslNltyNm"])
    try:
        print("ETA : " + item["details"]["detail"][0]["etryptDt"])
        print("내외항 : " + item["details"]["detail"][0]["ibobprtNm"] + "\n")
    except:
        print("ETA : " + item["details"]["detail"]["etryptDt"])
        print("내외항 : " + item["details"]["detail"]["ibobprtNm"] + "\n")
    i += 1

'''
file_path = "./sample.json"
with open(file_path, 'w', encoding='UTF-8') as outfile:
    json.dump(dict2_type, outfile, indent=4, ensure_ascii=False)
'''
