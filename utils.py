import sqlite3
import subprocess
import sys
import time
import random
# from config import USER_AGENTS_FILE
from ppadb.client import Client as AdbClient
import requests
import datetime
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()

# Get Random User Agent String.
user_agent = user_agent_rotator.get_random_user_agent()

def init_device():
    subprocess.call("adb devices", shell=True)
    deviceport = 5037
    client = AdbClient(host="127.0.0.1", port=deviceport)
    devices = client.devices()
    if len(devices) == 0:
        print("No devices attached")
        sys.exit()
    return devices[0]


def rate_limiter(last_run_time, min_interval_minutes):
    now = datetime.datetime.now()
    if last_run_time:
        time_since_last_run = (now - last_run_time).total_seconds() / 60
        if time_since_last_run < min_interval_minutes:
            time.sleep((min_interval_minutes - time_since_last_run) * 60)
    return now

def get_current_ip():
    try:
        response = requests.get("https://api64.ipify.org")
        if response.status_code == 200:
            print(response.text)
            return response.text
    except requests.RequestException as e:
        print(e)
        pass
    return ''



def send_keys_with_delay(element, text, min_delay=0.1, max_delay=0.3):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


def human_typing(element, text, delay=0.1):
    for char in text:
        time.sleep(delay)
        element.send_keys(char)


def human_like_scroll(driver, scroll_range=5, min_delay=0.5, max_delay=1.5, min_step=100, max_step=300):
    current_scroll_position, new_scroll_position = 0, 0

    for _ in range(scroll_range):
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        scroll_step = random.randint(min_step, max_step)
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position + scroll_step});")
        time.sleep(random.uniform(min_delay, max_delay))

        new_scroll_position = driver.execute_script("return window.pageYOffset;")
        if new_scroll_position == current_scroll_position:
            break


def db_operation(query, params=None, fetch=False):
    conn = sqlite3.connect("ohouse_log.db")
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch:
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None

    conn.close()
    return data

def init_device():
    subprocess.call("adb devices", shell=True)
    deviceport = 5037
    client = AdbClient(host="127.0.0.1", port=deviceport)
    devices = client.devices()
    if len(devices) == 0:
        print("No devices attached")
        sys.exit()
    return devices[0]


def random_user_agent():
    with open(USER_AGENTS_FILE, "r") as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()


def get_random_user_agent():
    user_agents = [
        # Add your list of User-Agents here

    ]
    return random.choice(user_agents)


def random_wait(min_sec=10, max_sec=20):
    time_to_sleep = random.uniform(min_sec, max_sec)
    print('랜덤시간 체류하기'+str(time_to_sleep))
    time.sleep(time_to_sleep)


#def change_ip(adb_path):
def change_ip_adb():
    print("Current IP: ")
    # get_current_ip()
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


def click_random_links(driver, num_clicks=2, min_delay=1, max_delay=2):
    for _ in range(num_clicks):
        try:
            links = driver.find_elements_by_css_selector("a")
            if not links:
                break

            random_link = random.choice(links)
            try:
                random_link.click()
                time.sleep(random.uniform(min_delay, max_delay))
                driver.back()
                time.sleep(random.uniform(min_delay, max_delay))
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass


def read_excel_file(file_name):
    df = pd.read_excel(file_name)
    return df
