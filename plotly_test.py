import urllib.request
from bs4 import BeautifulSoup
import plotly.graph_objects as go
 
def get_incheonpilot() :
    url = 'http://www.incheonpilot.com/pilot/pilot04_01.asp?Datepicker_date='
    date = input("날짜를 입력하시오.(작일까지의 데이터만 검색 가능합니다.)")
    req = urllib.request.urlopen(url+date)
    res = req.read()

    soup = BeautifulSoup(res,'html.parser')
    my_titles = soup.select( 'body > div > div > div > div > div > div > table > tr > td' ) 
    title = []
    i = 0

    for titles in my_titles :
        if i > 28 :
            title.append(str(titles.text).replace(u'\xa0', u' ').strip())
        i += 1
    i = 0
    value = []

    for i in range(12) :
        value.append([])

    for title_value in title :
        value[(i+1)%12].append(title_value)
        i += 1

    print(value)

    fig = go.Figure(data=[go.Table(header=dict(values=['No', '도선사', '시간', '선명', '갑문', '도선구간', '접안', '톤수', '홀수', '대리점', '예선', 'JOB NO']),
                    cells=dict(values=value))
                        ])
    fig.show()

get_incheonpilot()