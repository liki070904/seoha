from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
import time
import logging
import pyautogui

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def some_function():
    logging.info("some_function 호출됨")

# 드라이버 설정
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

# 관리자 홈페이지 입력
admin_homepage_url = "https://dev-munhak-manager.ntoday.kr/login"
# 문학동네 홈페이지 입력
homepage_url = "https://dev-munhak-home.ntoday.kr/"
# 독파 홈페이지 입력
dokpa_homepage_url = "https://dev-munhak-dokpa.ntoday.kr/"

html = urlopen(homepage_url)
soup = BeautifulSoup(html, "html.parser")

def home_page(driver, wait):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(homepage_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(3)

def close_popup(driver, wait):
    # popMainLayer가 나타날 때까지 기다림
    # while not driver.execute_script("return document.getElementById('popMainLayer1') !== null;"):
    #    time.sleep(1)  # 1초 대기 후 다시 확인
    popup_exists = driver.execute_script("return document.getElementById('popMainLayer1') !== null;")
    if popup_exists:
        close_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="popMainLayer1"]/div/div[2]/button[1]'))
            )
        # JavaScript로 클릭 시도
        driver.execute_script("arguments[0].click();", close_button)
    pyautogui.confirm(title = 'complete', text = '테스트 완료')
    time.sleep(10)

def test_web_application():
    driver, wait = setup_driver()
    some_function()
    try:
        home_page(driver, wait)
        print("문학동네 홈페이지 진입 성공")
    except Exception as e:
        logging.error(f"문학동네 홈페이지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        close_popup(driver, wait)
        print("close_popup")
    except Exception as e:
        logging.error(f"close_popup error: {str(e)}")
    finally:
        driver.quit()
    
if __name__ == "__main__":
    test_web_application()