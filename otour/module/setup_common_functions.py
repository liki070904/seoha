from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os

# path
def get_current_dir():
    """현재 파일이 위치한 디렉토리 반환"""
    return os.path.dirname(os.path.abspath(__file__))
def get_parent_dir(level=1):
    """현재 파일의 상위 디렉토리 반환 (기본적으로 한 단계 위)"""
    current_dir = get_current_dir()
    return os.path.abspath(os.path.join(current_dir, *[".."] * level))
# 요소가 보이는 영역 안에 있도록 스크롤하는 함수
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# 스크롤 최하단으로
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 클릭
def click(driver, element):
    driver.execute_script("arguments[0].click();", element)
# 예약조회 iframe
def iframe(driver, wait):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)
# 복지몰 취소요청 조회 iframe
def cancel_iframe(driver, wait):
    cancel_iframe_switch = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[4]/div/iframe')
    driver.switch_to.frame(cancel_iframe_switch)
# 드라이버 설정
def setup_driver():
    # Chrome WebDriver 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--force-device-scale-factor=0.9")
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # WebDriver 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 대기 설정
    driver.implicitly_wait = (10)
    wait = WebDriverWait(driver, 10)
    return driver, wait