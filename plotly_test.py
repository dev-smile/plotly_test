import urllib.request
from bs4 import BeautifulSoup
import plotly.graph_objects as go
 
def get_incheonpilot() :
    print("인천 도선사회 도선 예보 현황")
    date = input("날짜를 입력하시오. : ")
    url = 'http://www.incheonpilot.com/pilot/pilot04_01.asp?Datepicker_date='
    req = urllib.request.urlopen(url+date)
    res = req.read()

    soup = BeautifulSoup(res,'html.parser')
    my_titles = soup.select( 'body > div > div > div > div > div > div > table > tr > td' ) 
    title = []
    value = []
    i = 0

    for i in range(12) :
        value.append([])

    for titles in my_titles :
        if i > 39 :
            value[(i-28)%12].append(str(titles.text).replace(u'\xa0', u' ').strip())
        i += 1

    fig = go.Figure(data=[go.Table(header=dict(values=['No', '도선사', '시간', '선명', '갑문', '도선구간', '접안', '톤수', '홀수', '대리점', '예선', 'JOB NO']),
                    cells=dict(values=value))
                        ])
    fig.show()

get_incheonpilot()