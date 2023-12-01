import json
import os
import re
import shutil
import sys
import urllib

import mysql.connector
import chromedriver_autoinstaller
import mysql
import datetime
from adbutils._utils import current_ip
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import options, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import requests
import subprocess
from fake_useragent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import pysnooper
from ppadb.client import Client as AdbClient
from selenium.webdriver.common.by import By
from utils import user_agent


def init_device():
    subprocess.call("adb devices", shell=True)
    deviceport = 5037
    client = AdbClient(host="127.0.0.1", port=deviceport)
    devices = client.devices()
    if len(devices) == 0:
        print("No devices attached")
        sys.exit()
    return devices[0]

import requests

def get_current_ip_ipinfo():
    try:
        response = requests.get('https://ipinfo.io/json')
        ip = response.json()['ip']
        return ip
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

current_ip = get_current_ip_ipinfo()
print(f"현재 IP 주소: {current_ip}")


def change_ip_adb():
    print("Current IP: ")

    print("Changing IP...")
    try:
        device = init_device()

        device.shell("svc data disable")
        time.sleep(5)
        device.shell("svc data enable")
        time.sleep(5)
        print("New IP: ")
        # get_current_ip()
        print("IP changed successfully!")
    except Exception as e:
        print(e)
        subprocess.call("adb kill-server", shell=True)
        return

    return device.get_serial_no()  # return the device serial number



#undected chrome driver 시작
def init_driver():
    options=uc.ChromeOptions()
    print('init_driver 함수 실행')
    try :
        shutil.rmtree(r"C:\chrometemp")  #쿠키 / 캐쉬파일 삭제(캐쉬파일 삭제시 로그인 정보 사라짐)
    except FileNotFoundError :
        pass

    # try:
    #     subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
    #                      r'--user-data-dir="C:\chrometemp22"')  # 디버거 크롬 구동
    # except FileNotFoundError:
    #     subprocess.Popen(
    #         r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
    #         r'--user-data-dir="C:\chrometemp22"')
    #
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:

        options.add_argument("--auto-open-devtools-for-tabs")  # automatically open dev tools on every new tab
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--start-maximized')  # 브라우저가 최대화된 상태로 실행됩니다.
        from webdriver_manager.chrome import ChromeDriverManager
        #driver_exec_path = ChromeDriverManager().install()
        driver_exec_path = './119/chromedriver.exe'
        driver = uc.Chrome(driver_executable_path=driver_exec_path, options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        # driver = uc.Chrome(enable_cdp_events=True)
        try:
            driver.set_page_load_timeout(30)
        except Exception as e:
            print(e)
            pass

        # and of couse 2 lousy examples
        #driver.add_cdp_listener('Network.requestWillBeSent', mylousyprintfunction)
        # driver.add_cdp_listener('Network.dataReceived', mylousyprintfunction)

        return driver
    except Exception as e:
        print('init_driver 오류', e)


# def chrome_driver_setup():
#     # 크롬 버전 확인
#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#     chromedriver = f'./{chrome_ver}/chromedriver.exe'
#
#     # 크롬 드라이버가 설치되어 있지 않다면 설치
#     if not os.path.exists(chromedriver):
#         chromedriver_autoinstaller.install(True)
#
#     options = ChromeOptions()
#     # 크롬 드라이버 최신 버전 설정
#     service = ChromeService(executable_path=ChromeDriverManager().install())
#
#     # chrome driver
#     driver = webdriver.Chrome(service=service(ChromeDriverManager().install()))
#     return driver
# 랜덤 에이전트 설정

def random_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names,operating_systems=operating_systems, limit=100)

    # Get list of user agents.
    user_agents = user_agent_rotator.get_user_agents()
    print("현재user_agent",user_agents)
    user_agent = user_agent_rotator.get_random_user_agent()  # 실제 사용자 에이전트 문자열을 가져옵니다.
    print("바꾼 user_agent", user_agent)
    return user_agent

def get_product_list(keyword, url, max_iterations=30):
    # Extract sno from the user provided URL
    sno_to_find = re.search(r'/goods/(\d+)', url).group(1)

    next_token = None
    initial_iteration = True
    found = False  # Initialize 'found' here
    Rank = 0

    for iteration in range(max_iterations):
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://api.a-bly.com/api/v2/screens/SEARCH_RESULT/?query={encoded_keyword}&search_type=DIRECT&sorting_type=POPULAR"
        if next_token:
            search_url += f"&next_token={next_token}"

        user_agent = UserAgent()
        headers = {
            'authority': 'api.a-bly.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'origin': 'https://m.a-bly.com',
            'pragma': 'no-cache',
            'referer': 'https://m.a-bly.com/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent.random,  # 랜덤한 User-Agent를 사용합니다.
            'x-anonymous-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhbm9ueW1vdXNfaWQiOiIxNjM4NjU3OTUiLCJpYXQiOjE2OTk5NDcwMzB9.SOqLvOojj5O7pjzWOpG-IkzAZxYFnFr0xjpgVl1pFkc',
            'x-app-version': '0.1.0',
            'x-device-id': 'b8181251-fbe9-4094-bdff-312ab8dc4b77',
            'x-device-type': 'MobileWeb'

        }

        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)

            for component in data["components"]:
                if component.get("type", {}).get("item_list") == "THREE_COL_GOODS_LIST":
                    for item in component["entity"]["item_list"]:
                        Rank += 1
                        product = item["item"]
                        #print(Rank,product)


                       # adjusted_rank = iteration * len(component["entity"]["item_list"]) + component["entity"][
                        #    "item_list"].index(item) + 1
                        #print(adjusted_rank,product)
                        if str(product["sno"]) == sno_to_find:
                           # print(adjusted_rank,sno={product['sno']},market_name={product['market_name']})
                            print(f"Found your product: Rank: {Rank}, sno={product['sno']}, market_name={product['market_name']}, item_name={product['name']}")
                            #print(type(Rank))
                            found = True
                            break

                if found:
                    break

            if found:
                break

            next_token = data.get("next_token", None)
            if not next_token:
                print("No more data or Next Token not found. Ending process.")
                break
        else:
            print("Error fetching data. Status code:", response.status_code)
            break

    if not found:
        print(f"Product with sno {sno_to_find} not found in the search results.")
    return found, Rank, next_token
    #요청에 대한 재시도 메커니즘
# def get_url_data(keyword, link, max_retries=10):
#     retries = 0
#     product_id = link.split('/')[-1]  # '11560430' 추출
#     print(type(product_id))
#     while retries < max_retries:
#         change_ip_adb()  # IP 변경 시도
#         # 데이터 슬롯 함수 호출
#         driver, success = data_slot(keyword, link, product_id)
#     if success:
#         break
#     else:
#         print(f"Attempt {retries + 1} failed. Retrying...")
#         if driver:
#             driver.quit()  # 현재 열린 브라우저 창을 닫음
#         retries += 1
#         time.sleep(5)
#
#     if not success:
#         raise Exception("Failed to complete data_slot after multiple attempts")
#     elif driver:
#         driver.quit()  # 성공한 경우에도 브라우저 창을 닫음
# def get_url_data(keyword, link, max_retries=10):
#     retries = 0
#     product_id = link.split('/')[-1]  # '11560430' 추출
#     print(type(product_id))
#
#     while retries < max_retries:
#         change_ip_adb()  # IP 변경 시도
#         success = data_slot(keyword, link, product_id)  # 데이터 슬롯 함수 호출
#
#         if success:
#             break  # 성공 시 반복문 종료
#         else:
#             print(f"Attempt {retries + 1} failed. Retrying...")
#             if driver:
#                 driver = undetected_chromedriver.Chrome()
#                 driver.quit()  # 현재 열린 브라우저 창을 닫음
#             retries += 1
#             time.sleep(5)
#
#     if not success:
#         raise Exception("Failed to complete data_slot after multiple attempts")
#     elif driver:
#         driver.quit()  # 성공한 경우에도 브라우저 창을 닫음

# def get_url_data(driver,keyword, url, max_retries=10):
#     retries = 0
#     product_id = url.split('/')[-1]  # '11560430' 추출
#     print(type(product_id))
#
#     while retries < max_retries:
#         # change_ip_adb()  # IP 변경 시도
#         time.sleep(5)
#         ua = UserAgent()
#         useragent = ua.random
#         driver = init_driver()
#         success = data_slot(driver,keyword, url, product_id)  # 데이터 슬롯 함수 호출
#
#         if success:
#             break  # 성공 시 반복문 종료
#         else:
#             print(f"Attempt {retries + 1} failed. Retrying...")
#             if driver:  # Check if driver is not None
#                 driver.quit()  # 현재 열린 브라우저 창을 닫음
#             retries += 1
#             time.sleep(5)
#
#     if driver:  # Check if driver is not None
#         driver.quit()  # 성공한 경우에도 브라우저 창을 닫음

@pysnooper.snoop()
def data_slot(driver,keyword,url,Rank):
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    #get_product_list(keyword, url,Rank,max_iterations=30)
    product_id = url.split('/')[-1]  # '11560430' 추출
    success = False  # 성공 여부를 나타내는 플래그 변수1
    try:
            print("인스턴스 생성완료")
            # driver.implicitly_wait(20)  # 예: 10초 동안 대기
            # https://m.a-bly.com/ 접속
            driver.get("https://m.a-bly.com/")
            print("Successfully accessed the website")  # Successfully accessed the website

            time.sleep(20)
            # 첫 번째 요소 클릭
            # driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[1]/div').click()
            try:
                wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
                element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[viewBox='0 0 20 20']")))
                element.click()
            except Exception as e:
                print("에러발생",e)
            # 5초 대기
            time.sleep(10)

            # 요소 찾기
            search_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.sc-8b721f4d-2.kCBYFq"))
            )

            # 요소 클릭
            search_element.click()

            # 텍스트 입력
            search_element.send_keys(keyword)
            search_element.send_keys(Keys.RETURN)

            # 5초 대기
            time.sleep(5)

            # 주어진 링크로 접속
            #필터 클릭
            driver.find_element(By.CSS_SELECTOR, "#root > div > div > div.sc-d8a0b042-0.eVmIiV > div.sc-b6434c82-0.iaITWs > div > ul > li:nth-child(1) > div").click()
            print("필터 클릭 했음")
            time.sleep(5)
            #인기순 체크박스 클릭
            driver.find_element(By.CSS_SELECTOR,"#root > div.sc-baef2181-0.hsbGZQ.sc-b88b4070-5.clba-dr.sc-90c342b5-0.ihHGPr > div.sc-b88b4070-2.cegVEd > div > div > div.sc-79c0b905-0.gzBNem > div > div > div:nth-child(2) > div").click()
            print("인기순 체크박스 클릭함")
            #결과 보기 클릭
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR,
                                "#root > div.sc-baef2181-0.hsbGZQ.sc-b88b4070-5.clba-dr.sc-90c342b5-0.ihHGPr > div.sc-b88b4070-3.zkuwn > div > button.sc-90c342b5-2.jJDjxT.button.button__fill.button__medium.button__solid__pink.typography__subtitle2").click()
            print("결과보기 찍음")
            #driver.get(url)
            # 스크롤 위치 계산
            row_number = (Rank - 1) // 3  # Rank를 3으로 나누어 줄 번호를 계산 (0부터 시작)
            scroll_distance = row_number * 186.66
            print(f"Scrolling to row {row_number}, distance: {scroll_distance}")

            # 스크롤
            driver.execute_script(f"window.scrollTo(0, {scroll_distance});")
            print('Scrolling...')
            time.sleep(30)  # 스크롤 후 대기

            # 상품 클릭
            product_index = (Rank - 1) % 3  # 같은 줄 내에서의 상품 위치
            products = driver.find_elements(By.CLASS_NAME, "sc-ecca1885-2")
            row_products = products[row_number * 3: (row_number + 1) * 3]  # 해당 줄의 상품들
            if product_index < len(row_products):
                ActionChains(driver).move_to_element(row_products[product_index]).click().perform()
                print(f"Clicked product at rank {Rank} (row {row_number}, position {product_index + 1})")
            else:
                print(f"Product at rank {Rank} not found")
            success = True

    except requests.RequestException as e:
        print(f"Failed to access '{url}' using requests. Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print(f"작업 성공 여부: {success}")
        if success:
            log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = (current_ip, user_agent, url, product_id, keyword, Rank)
            print(data)
            save_to_database(data)
            driver.quit()
        else:
            print("작업에 실패하였습니다")
            #
    #         #driver.back()
    #         #뒤로가기 버튼 클릭
    #         success = True
    #         print(f"작업완료 '{keyword}' and link '{url}'")
    #         # 성공한 경우 플래그를 True로 설정
    # except requests.RequestException as e:  # requests 라이브러리에서 발생하는 모든 예외를 처리합니다.
    #         print(f"Failed to access '{url}' using requests. Error: {str(e)}")
    #
    # finally:
    #     print(f"작업 성공 여부: {success}")
    #     if success:
    #         # 현재 시간을 YYYY-MM-DD HH:MM:SS 형식으로 가져오기
    #         log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         data = (current_ip, user_agent, url, product_id, keyword,Rank)  # 여기서 ip와 user_agent를 사용합니다.
    #         print(data)
    #         save_to_database(data)
    #         print(data)
    #         driver.quit()
    #     else:
    #         print("작업에 실패하였습니다")

from selenium.webdriver.common.action_chains import ActionChains


# def search_and_click_product(driver, keyword, rank):
#     product_height = 186.66
#     # 검색 입력 필드 찾기
#     search_element = driver.find_element(By.CSS_SELECTOR, "input.sc-8b721f4d-2.kCBYFq")
#     search_element.clear()
#     search_element.send_keys(keyword)
#     search_element.send_keys(Keys.RETURN)
#
#     # 페이지 로딩 대기
#     time.sleep(5)  # 필요에 따라 WebDriverWait를 사용하여 요소가 로드될 때까지 기다릴 수 있습니다.
#
#     # 스크롤 위치 계산
#     scroll_distance = rank * product_height
#
#     # 스크롤
#     driver.execute_script(f"window.scrollTo(0, {scroll_distance});")
#
#     # 스크롤 후 적절한 대기 시간 추가
#     time.sleep(3)

def save_to_database(data):
    connection = None  # Declare connection variable
    with open('config_mysql.json') as f:
        config = json.load(f)
    db_host = config['db_host']
    db_user = config['db_user']
    db_password = config['db_password']
    db_name = config['db_name']

    try:
        connection = mysql.connector.connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_password)
        print("db connection")
        if connection.is_connected():
            print("DB 연결 성공")
            cursor = connection.cursor(prepared=True)
            # 쿼리 수정: log_time 컬럼에 현재 시간을 삽입
            query = """INSERT INTO sys.ably_log (log_time, current_ip, user_agent, url, product_id, keyword,Rank) VALUES (NOW(),%s, %s, %s, %s, %s,%s)"""
            print("쿼리 작성 완료")
            # data 튜플이 (current_ip, user_agent, url, product_id, keyword) 순서로 되어 있어야 함
            cursor.execute(query, data)
            print("쿼리 실행 완료")
            connection.commit()
            print("데이터베이스에 로그 저장 완료")
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


# def save_to_database(data):
#     with open('config_mysql.json') as f:
#         config = json.load(f)
#     db_host = config['db_host']
#     db_user = config['db_user']
#     db_password = config['db_password']
#     db_name = config['db_name']
#
#     try:
#         connection = mysql.connector.connect(host=db_host,
#                                              database=db_name,
#                                              user=db_user,
#                                              password=db_password)
#         if connection.is_connected():
#             cursor = connection.cursor()
#             query = """INSERT INTO ably (current_ip, user_agent, keyword, url) VALUES (%s, %s, %s, %s)"""
#             cursor.execute(query, data)
#             connection.commit()
#             print("Data successfully saved to database")
#     except mysql.connector.Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()


if __name__ == '__main__':

    keywords_urls = [
        ('거북이','https://m.a-bly.com/goods/5303035'),
        ('미니원피스','https://m.a-bly.com/goods/12159753')

    ]
while True:
    for keyword, url in keywords_urls:
            change_ip_adb()
            get_current_ip_ipinfo()
            print(f"Processing keyword: {keyword}, url: {url}")
            driver = init_driver()
            found, Rank, next_token = get_product_list(keyword, url, max_iterations=30)
            data_slot(driver, keyword, url,Rank)  # Pass Rank to data_slot