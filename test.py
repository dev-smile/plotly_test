from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import xmltodict

url = 'http://apis.data.go.kr/1192000/VsslEtrynd2/Info'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3+6o3M4O1nW6YMdRw==', \
                                quote_plus('pageNo') : '1', \
                                quote_plus('numOfRows') : '10', \
                                quote_plus('prtAgCd') : '030', \
                                quote_plus('sde') : '20210629', \
                                quote_plus('ede') : '20210630', \
                                quote_plus('clsgn') : '' } \
                              )

req = urlopen(url + queryParams)
res = req.read().decode('utf8')
dict_type = xmltodict.parse(res)
print(dict_type)


