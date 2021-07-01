# 크롤링 하여 Plotly Table 로 출력

# 크롤링
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
# plotly
import plotly.graph_objects as go

def get_incheonpilot() -> None:
    # crawled from 인천항 도선사회 - 도선 예보 현황
    print("인천 도선사회 도선 예보 현황")
    date = input("날짜를 입력하시오.(YYYY-MM-DD) : ")
    url = 'http://www.incheonpilot.com/pilot/pilot04_01.asp?Datepicker_date='
    req = urllib.request.urlopen(url + date)
    res = req.read()

    soup = BeautifulSoup(res, 'html.parser')
    my_titles = soup.select('body > div > div > div > div > div > div > table > tr > td')
    value = []
    i = 0

    # 이중 list 선언
    for i in range(12):
        value.append([])

    for titles in my_titles:
        if i > 39:
            # 이전까지는 다른 테이블 데이터
            value[(i - 40) % 12].append(str(titles.text).replace(u'\xa0', u' ').strip())
        i += 1

    # plotly table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=['No', '도선사', '시간', '선명', '갑문', '도선구간', '접안', '톤수', '홀수', '대리점', '예선', 'JOB NO']),
                cells=dict(values=value)
            )
        ]
    )
    fig.show()


def get_vesselfinder() -> None:
    # crawled from VesselFinder
    # 셀레니움 사용, 크롬 드라이버 설정
    driver = webdriver.Chrome('chromedriver')

    url = 'https://www.vesselfinder.com/ports/KRINC001'

    driver.get(url)

    sel = driver.page_source
    soup = BeautifulSoup(sel, 'html.parser')

    vesselfinder_soup = soup.find('div', id='tab-content')

    print('[ 1: expected, 2: arrivals, 3: departures, 4: in-port ]')
    select = 0
    select_id = ''

    while select > 5 or select < 1:
        select = int(input("메뉴를 선택하시오. : "))
        if select == 1:
            select_id = 'expected'
        elif select == 2:
            select_id = 'arrivals'
        elif select == 3:
            select_id = 'departures'
        elif select == 4:
            select_id = 'in-port'
        else:
            print("다시 입력하시오.")

    selected_soup = vesselfinder_soup.find('section', id=select_id)
    value = []

    for i in range(6):
        value.append([])

    # VesselFinder 에서는 값을 20개만 보여준다.
    for i in range(20):
        middle_data = selected_soup.select("table > tbody > tr")[i]
        value[0].append(middle_data.select('td')[0].text) # 'ETA'
        value[2].append(middle_data.select('td')[2].text) # 'Built'
        value[3].append(middle_data.select('td')[3].text) # 'GT'
        value[4].append(middle_data.select('td')[4].text) # 'DWT
        value[5].append(middle_data.select('td')[5].text) # 'Size (m)'

    vessel = selected_soup.find_all('div', class_='named-title')

    for titles in vessel:
        value[1].append(str(titles.text).strip()) # 'Vessel'

    driver.quit()

    # plotly table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=['ETA', 'Vessel', 'Built', 'GT', 'DWT', 'Size (m)']),
                cells=dict(values=value)
            )
        ]
    )
    fig.show()


if __name__ == "__main__":
    #get_incheonpilot()
    get_vesselfinder()
