# 문제 1. 벅스뮤직에서 전체 순위 가져오고, 순위에 따라 점수 매기기
# 순위에 따라서 점수 부여
# 1등 -> 100점, 100등 -> 1점
# 특정 기간내에 차트 진입 점수 계산
# 예) 15일간 차트 분석 
# 12월12 일 -> 아이유 150 점, 12월 11일 -> 아이유 160점, 12월 1일  아이유 누적점수 ~~점
# 누적된 점수별 아티스트 계산  상위 10명 을 히스토 그램으로 그려 보세요.

# --------------- 내 풀이 ---------------------

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://music.bugs.co.kr/chart/track/day/total"
bugs_raw = requests.get(url)
soup = BeautifulSoup(bugs_raw.text,"html.parser")

# 1등 가져오기
bugs_winner = soup.find("a",adultcheckval="1")
print("1등 : ",bugs_winner.text)

# 전체 순위 가져오고, 순위에 따라 점수 매기기
# 순위에 따라서 점수 부여
# 1등 -> 100점, 100등 -> 1점

bugs_sing = soup.find_all("p",class_="title")
bugs_artist = soup.find_all("p",class_="artist")
rate_score = []
count = 0

for i,j in zip(bugs_sing, bugs_artist):
    count +=1
    rate_score.append(101-count)
    print(count, "위",i.text,j.text,"\n", rate_score[count-1],"\n")


# 특정 기간내에 차트 진입 점수 계산
# 예) 15일간 차트 분석 
# 12월12 일 -> 아이유 150 점, 12월 11일 -> 아이유 160점, 12월 1일  아이유 누적점수 ~~점
# 누적된 점수별 아티스트 계산  상위 10명 을 히스토 그램으로 그려 보세요.

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day

day_count = []
for i in range(15):
    dc_day = day -i
    dc_month = month
    dc_year = year
    if dc_day < 1:
        dc_month-=1
        dc_day+=30
    day_count.append(dc_year*10000+dc_month*100+dc_day)


chart = []
for i in day_count:
    url = "https://music.bugs.co.kr/chart/track/day/total?chartdate=" + str(i)
    bugs_raw = requests.get(url)
    bugs_soup = BeautifulSoup(bugs_raw.text,"html.parser")
    bugs_date = i
    bugs_sing = soup.find_all("p",class_="title")
    bugs_artist = soup.find_all("p",class_="artist")
    rate_score = []
    count = 0
    for j,k in zip(bugs_sing, bugs_artist):
        count +=1
        rate_score.append(101-count)
        chart.append({"title":j.text.replace("\n", " "),
                    "artist":k.text.replace("\n", " "),
                    "date":bugs_date,"rate":count,
                    "score":rate_score[count-1]})
    

bugs = pd.DataFrame(chart)
bugs_top = bugs.groupby("title").sum().sort_values(by="score", ascending=False).head(10)


# -------------------- 여기서부터 강사님 풀이 ------------------------

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://music.bugs.co.kr/chart/track/day/total?chartdate=" 
url = url + str(20221204)

html = requests.get(url)
soup = bs(html.text, "html.parser")

bugs_day=[]
tbody=soup.find("tbody")
tr_soup=tbody.find_all("tr")

for tr in tr_soup:
    rank=tr.find("div", class_="ranking").get_text().split("\n")[1]
    title=tr.find("p", class_="title").get_text().replace("\n", "")
    art=tr.find("p", class_="artist").get_text().replace("\n", "")
    album=tr.find("a", class_="album").get_text().replace("\n", "")
    bugs_day.append([rank, title, art, album])
    
# bugs_day
df=pd.DataFrame(bugs_day, columns=["순위", "곡명", "아티스트", "앨범"])
df.info()

# 순위에 따라서 점수 부여
# 1등 -> 100점, 100등 -> 1점
score=[]
for i in range(100):
    score.append(101-int(df.loc[i, "순위"]))
df["점수"]=score
df


# 시작일부터 종료일까지 날짜 입력후 list로 생성
from tqdm import tqdm
import pandas as pd
sdt=input("시작일 입력:")
edt=input("종료일 입력:")

dates=pd.date_range(sdt, edt)
dates=[i.strftime("%Y%m%d") for i in dates]
#print(dates)

df_bugs=pd.DataFrame()

for date in tqdm(dates):
    url="https://music.bugs.co.kr/chart/track/day/total?chartdate=" + str(date)
    
    html=requests.get(url)
    soup = bs(html.text, "html.parser")
    
    bugs_day=[]
    tbody=soup.find("tbody")
    tr_soup=tbody.find_all("tr")
    
    scr=101   # 점수 초기값
    for tr in tr_soup:
        rank=tr.find("div", class_="ranking").get_text().split("\n")[1]
        title=tr.find("p", class_="title").get_text().replace("\n", "")
        art=tr.find("p", class_="artist").get_text().replace("\n", "")
        album=tr.find("a", class_="album").get_text().replace("\n", "")
        scr -= 1  # 1회 추출시 -1 만큼 감소
        bugs_day.append([date, rank, title, art, album, scr])

    # bugs_day
    df=pd.DataFrame(bugs_day, columns=["날짜", "순위","곡명","아티스트",
                                       "앨범","점수"])
    df_bugs=pd.concat([df_bugs, df])
    
df_bugs.reset_index(drop=True, inplace=True) 
#df_bugs=df_bugs.reset_index(drop=True)
df_bugs.info()


# 특정 기간내에 차트 진입 점수 계산
# 예) 15일간 차트 분석 
# 12월12 일 -> 아이유 150 점, 12월 11일 -> 아이유 160점, 12월 1일  아이유 누적점수 ~~점
# 누적된 점수별 아티스트 계산  상위 10명 을 히스토 그램으로 그려 보세요.

df_bugs_top = df_bugs.groupby(["아티스트"]).sum().sort_values("점수", ascending=False).head(10)

import matplotlib.pyplot as plt
import platform

plt.rc('font', family = "NanumMyeongjo")

plt.style.use('ggplot')
plt.figure(figsize=(10, 4))
plt.xticks(size=9, rotation=45)
plt.bar(df_bugs_top.index, df_bugs_top["점수"])
plt.title(f"12월 가장 많이 나타난 아티스트(기간:{sdt}~{edt})", size=15)
plt.ylabel("점수")
plt.show()

df_bugs_values = df_bugs.groupby(["아티스트","날짜"]).sum().sort_values("점수", ascending=False)
df_bugs_values_top = df_bugs_values.loc[df_bugs_top.index]
df_bugs_values_top = df_bugs_values_top.reset_index()
df_bugs_values_top_pivot = df_bugs_values_top.pivot("아티스트","날짜","점수")
df_bugs_values_top_pivot.fillna(0)

df_bugs_values_top_pivot.plot(kind="bar", stacked=True, figsize=(20, 30)) 