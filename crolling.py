import requests
import time
import random
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def select_local():
    local_dict = {
        1: '서울',
        2: '경기',
        3: '충북',
        4: '충남',
        5: '경북',
        6: '경남',
        7: '전북',
        8: '전남',
        9: '강원',
        10: '제주',
        11: '인천',
        12: '부산',
        13: '대구',
        14: '대전',
        15: '울산',
        16: '광주',
        17: '세종'
    }
    print("1. 서울")
    print("2. 경기")
    print("3. 충북")
    print("4. 충남")
    print("5. 경북")
    print("6. 경남")
    print("7. 전북")
    print("8. 전남")
    print("9. 강원")
    print("10. 제주")
    print("11. 인천")
    print("12. 부산")
    print("13. 대구")
    print("14. 대전")
    print("15. 울산")
    print("16. 광주")
    print("17. 세종")

    select_number = int(input("선택하실 지역 번호를 입력: "))
    if select_number in local_dict:
        return local_dict[select_number]
    else:
        print('번호가 올바르지 않습니다')
        return select_local()

def get_keywords():
    return ['건축','조경','토목','건설']

local = select_local()
keywords = get_keywords()

options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
driver = webdriver.Chrome(options=options)

wait_time = random.uniform(3, 5)

for keyword in keywords:
    url = f'https://bizno.net/?area={local}&query={keyword}'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'}
    response = requests.get(url, headers=header)
    html = response.text
    driver.get(url)
    time.sleep(2)

    filename = f'data_{local}_{keyword}.csv'

    # 해당 키워드에 대한 결과 수 확인
    result_count = len(driver.find_elements(By.XPATH, '//div[@class="single-post d-flex flex-row"]'))

    # 결과가 없는 경우 다음 키워드로 이동
    if result_count == 0:
        print(f"No results found for the keyword: {keyword}")
        continue

    with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
        fieldnames = ['업체 이름', '대표자','종목', '사업자 번호', '회사주소','우편번호','전화번호']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, result_count + 1):
            xpath = f'//div[@class="single-post d-flex flex-row"][{i}]//a/h4'
            element = driver.find_element(By.XPATH, xpath)

            scroll_script = """
                var element = arguments[0];
                element.scrollIntoView();
                window.scrollBy(0, arguments[1]);
            """
            driver.execute_script(scroll_script, element, -150)  # 예시로 50px만큼 아래로 스크롤합니다.

            time.sleep(1)
            element.click()
            time.sleep(wait_time)
            driver.set_window_size(2000, 2700)

            try:
                h1_text = driver.execute_script('return document.querySelector(".titles h1").innerText')
            except Exception as e:
                h1_text = "N/A"

            try:
                number = driver.find_element(By.XPATH, '//th[contains(text(), "사업자등록번호")]/following-sibling::td').text
            except NoSuchElementException:
                number = "N/A"
            try:
                section = driver.find_element(By.XPATH, '//th[contains(text(), "종목")]/following-sibling::td').text
            except NoSuchElementException:
                section = "N/A"
            try:
                adress = driver.find_element(By.XPATH, '//th[contains(text(), "회사주소")]/following-sibling::td').text
            except NoSuchElementException:
                adress = "N/A"
            try:
                adr_num = driver.find_element(By.XPATH, '//th[contains(text(), "우편번호")]/following-sibling::td').text
            except NoSuchElementException:
                adr_num = "N/A"

            try:
                boss = driver.find_element(By.XPATH, '//th[contains(text(), "대표자명")]/following-sibling::td').text
            except NoSuchElementException:
                boss = "N/A"

            try:
                tel = driver.find_element(By.XPATH, '//th[contains(text(), "전화번호")]/following-sibling::td/a').text
            except NoSuchElementException:
                tel = "N/A"

            if '*' in adress or section =="N/A":
                print("수집하지 않습니다")
                driver.back()
                time.sleep(wait_time)
                continue

            writer.writerow({'업체 이름': h1_text, '대표자': boss,'종목': section, '사업자 번호': number, '회사주소': adress, '우편번호': adr_num, '전화번호': tel})
            driver.back()
            time.sleep(wait_time)

print("크롤링이 완료되었습니다.")
