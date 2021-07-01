import time
import urllib.request
import json
from urllib.request import urlretrieve
import time
from urllib.error import HTTPError
from urllib.error import URLError

url = 'http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit?' \
      'serviceKey=Kk6GfZmcpKlmvK0ufG8JnZs8nZhJhSjiEWY6Qs6SoOdLkZLcdNam6Fv8JJBMVKJaXUkCz3%2B6o3M4O1nW6YMdRw%3D%3D&' \
      'pageNo=1&numOfRows=10&dataType=JSON&sat=G2&' \
      'data=vi006&area=ko&time=20210630'
req = urllib.request.urlopen(url)
res = req.read()

json_object = json.loads(res)
json_object2 = json_object.get('response').get('body').get('items').get('item')[0].get('satImgC-file')
json_object3 = json_object2[1:-1].split(',') # 주소값이 담긴 리스트 모양의 하나의 큰 문자열로 되어있음
i = 0

for image in json_object3:
    try:
        urlretrieve(image.strip(), "C:/Users/LeeJunHo/Documents/GitHub/test/image/image"+str(i)+".png")
        i += 1
        #time.sleep(0.5)
        print("download :", i)
    except HTTPError as e:
        print("HTTPError :", e)
    except URLError as e:
        print("URLError :", e)

# 조절 없는 요청으로 서버 측에서 에러 발생
# urllib.error.HTTPError: HTTP Error 500: Internal Server Error
# http.client.RemoteDisconnected: Remote end closed connection without response

