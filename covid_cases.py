import requests
import time
from bs4 import BeautifulSoup
import json
import os

url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"

info = {}

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html5lib')

taiwan = soup.body.find_all('div', attrs={'class': 'col-lg-3 col-sm-6 col-6 text-center my-5'})
count = 0
info['Taiwan'] = {"url": "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"}
for tw in taiwan:
    if count == 0:
        total_cases = tw.h1.get_text().strip()
        # local_cases = tw.p.get_text().split("本土病例 ")[1].strip()
        info['Taiwan'].update({"Total cases": total_cases}) # "Local cases": local_cases})
    elif count == 1:
        daily_cases = tw.h1.get_text().strip()
        # daily_local_cases = tw.p.get_text().split("本土病例 ")[1].strip()
        info['Taiwan'].update({"Daily cases": daily_cases}) # "Local daily cases": daily_local_cases})
    elif count == 2:
        total_death = tw.h1.get_text().strip()
        death_cases = tw.p.get_text().strip().split("\n")[0]
        info['Taiwan'].update({"Total deaths": total_death, "Death cases": death_cases})
    elif count == 3:
        total_vacc = tw.h1.get_text().strip()
        daily_vacc = tw.p.get_text().strip().split("\n")[0]
        doses = tw.p.get_text().strip().split("\n")[1].strip()
        first_dose = doses.split("(第一劑 ")[1].split(",")[0].strip()
        sec_dose = doses.split("(第一劑 ")[1].split(", 第二劑 ")[1].split(")")[0].strip()
        info['Taiwan'].update({"Total vaccinated": total_vacc, "Daily vaccinated": daily_vacc, "First dose": first_dose, "Second dose": sec_dose})
    count += 1

# print(info)
cities = soup.body.find_all('a', attrs={'class': 'btn btn-success btn-lg'})
city_list = ["New Taipei City", "Taipei City", "Taoyuan City", "Miaoli County", "Keelung City",\
            "Changhua County", "Taichung City", "Yilan County", "Hsinchu County", "Hualien County",\
            "Kaohsiung City", "Tainan City", "Hsinchu City", "Pingtung County", "Nantou County", "Taitung County",\
            "Yunlin County", "Chiayi County", "Chiayi City", "Penghu County", "Lienchiang County", "Kinmen County"]
# city_list = ["New Taipei", "Taipei", "Taoyuan", "Miaoli", "Keelung",\
#              "Changhua", "Taichung", "Yilan County", "Hsinchu County", "Hualien County",\
#              "Kaohsiung City", "Tainan City", "Hsinchu City", "Pingtung County", "Nantou County", "Taitung County",\
#              "Yunlin County", "Chiayi County", "Chiayi City", "Penghu County", "Lienchiang County", "Kinmen County"]
cities_eng = {}
cities_zh = {}
for idx, city in enumerate(city_list):
    cities_eng[idx] = city

city_list = ["新北市", "台北市", "桃園市", "苗栗縣", "基隆市", "彰化縣", "台中市", "宜蘭縣", "新竹縣",\
             "花蓮縣", "高雄市", "台南市", "新竹市", "屏東縣", "南投縣", "台東縣", "雲林縣", "嘉義縣",\
             "嘉義市", "澎湖縣", "連江縣", "金門縣"]
count = 0
for city in city_list:
    cities_zh[city] = count
    count += 1

# print(cities_eng)
# print(cities_zh)

for city in cities:
    link = "https://covid-19.nchc.org.tw/"
    link += city['href']
    tmp = city.get_text().split(" ")[0].strip()
    city_name = cities_eng[cities_zh[tmp]]
    info[city_name] = {"url": link}
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html5lib')
    city_info = soup.body.find_all('div', attrs={'class': 'col-lg-3 col-sm-6 col-6 text-center my-5'})
    count = 0
    for information in city_info:
        if count == 0:
            total_cases = information.h1.get_text().strip()
            info[city_name].update({"Total cases": total_cases})
        elif count == 1:
            daily_cases = information.h1.get_text().strip()
            info[city_name].update({"Daily cases": daily_cases})
        elif count == 2:
            first_dose = information.h1.get_text().strip()
            info[city_name].update({"First dose": first_dose})
        elif count == 3:
            sec_dose = information.h1.get_text().strip()
            info[city_name].update({"Second dose": sec_dose})
        count += 1
# print(info)

json_obj = json.dumps(info, indent=3)
# print(file)

with open("./covid_reports.json", "r+") as file:
    if os.stat("./covid_reports.json").st_size == 0:
        #print("file is empty!")
        file.write(json_obj)
    else: 
        #print("file is not empty!")
        data = json.loads(file.read())
        #print(type(data))
        data.update(info)
        file.truncate(0)
        file.seek(0)
        json_obj = json.dumps(info, indent=3)
        file.write(json_obj)

