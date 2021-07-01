import time
import urllib.request
import json
from urllib.request import urlretrieve
import time

url = 'http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit?' \
      'serviceKey=Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3%2B6o3M4O1nW6YMdRw%3D%3D&' \
      'pageNo=1&numOfRows=10&dataType=JSON&sat=G2&' \
      'data=vi006&area=ko&time=20210630'
req = urllib.request.urlopen(url)
res = req.read()

json_object = json.loads(res)
json_object2 = json_object.get('response').get('body').get('items').get('item')[0].get('satImgC-file')
json_object3 = json_object2[1:-1].split(',')
i = 0

for image in json_object3:
    urlretrieve(image.strip(), "C:/Users/LeeJunHo/Documents/GitHub/test/image/image"+str(i)+".png")
    i += 1
    time.sleep(0.5)
    print("download :", i)

# urllib.error.HTTPError: HTTP Error 500: Internal Server Error

