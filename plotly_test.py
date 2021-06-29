import urllib.request
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from selenium import webdriver
 
"""

value = plotly 테이블의 값 배열
"""

def get_incheonpilot() :
    print("인천 도선사회 도선 예보 현황")
    date = input("날짜를 입력하시오. : ")
    url = 'http://www.incheonpilot.com/pilot/pilot04_01.asp?Datepicker_date='
    req = urllib.request.urlopen(url+date)
    res = req.read()

    soup = BeautifulSoup(res,'html.parser')
    my_titles = soup.select( 'body > div > div > div > div > div > div > table > tr > td' ) 
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

def get_vesselfinder() : 
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome('chromedriver', options=options)

    url = 'https://www.vesselfinder.com/ports/KRINC001'

    driver.get(url)
    driver.implicitly_wait(0.3)

    sel = driver.page_source
    soup = BeautifulSoup(sel, 'html.parser')

    vesselfinder_soup = soup.find('div', id='tab-content')

    print('[ 1: expected, 2: arrivals,  3: departures, 4: in-port ]')
    select = 0
    select_id = ''

    while select > 5 or select < 1 :
        select = int(input("메뉴를 선택하시오. : "))
        if select == 1:
            select_id = 'expected'
        elif select == 2:
            select_id = 'arrivals'
        elif select == 3:
            select_id = 'departures'
        elif select == 4:
            select_id = 'in-port'

    selected_soup = vesselfinder_soup.find('section', id=select_id)
    value = []

    for i in range(6) :
        value.append([])

    for i in range(20) :
        middle_data = selected_soup.select("table > tbody > tr")[i]
        value[0].append(middle_data.select('td')[0].text)
        value[2].append(middle_data.select('td')[2].text)
        value[3].append(middle_data.select('td')[3].text)
        value[4].append(middle_data.select('td')[4].text)
        value[5].append(middle_data.select('td')[5].text)

    vessel = selected_soup.find_all('div', class_ = 'named-title')

    for titles in vessel :
        value[1].append(str(titles.text).strip())

    driver.quit()

    print(value)

    fig = go.Figure(data=[go.Table(header=dict(values=['ETA', 'Vessel', 'Built', 'GT', 'DWT', 'Size (m)']),
                        cells=dict(values=value))
                            ])
    fig.show()



if __name__ == "__main__":
    get_incheonpilot()
    get_vesselfinder()