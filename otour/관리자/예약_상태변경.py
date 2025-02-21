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
import time
import logging
import pyautogui

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def some_function():
    logging.info("some_function 호출됨")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--log-level=3')  # 로그 레벨 조정
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 30)
    return driver, wait

# 관리자 URL
admin_url = "https://devfss.hanatourbiz.com/login"
html = urlopen(admin_url)
soup = BeautifulSoup(html, "html.parser")

def manager_login(driver, wait):
    # 새 탭 열기
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    # 메인 페이지 접속
    driver.get(admin_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    # 채널 선택 드롭다운 클릭
    channel_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nice-select.sel_md")))
    channel_select.click()
    time.sleep(0.5)
    # '오투어' (2) 옵션 선택
    otour_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.option[data-value='2']")))
    otour_option.click()
    time.sleep(0.5)
    # ID 입력
    username = wait.until(EC.presence_of_element_located((By.ID, "userId")))
    username.clear()
    time.sleep(0.5)
    username.send_keys("wlocos")
    # 비밀번호 입력
    password = wait.until(EC.presence_of_element_located((By.NAME, "userPw")))
    password.clear()
    time.sleep(0.5)
    password.send_keys("hanabiz!@#")
    # 로그인 버튼 클릭
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogin")))
    login_button.click()
    # 로그인 후 대기
    time.sleep(1)

def channel_reserve_management(driver, wait):
    # 1. '예약관리' 메뉴 클릭
    reserve_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_book")))
    reserve_menu.click()
    time.sleep(0.5)
    # 2. '채널예약관리' 서브메뉴 클릭
    channel_reserve = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '채널예약관리')]")))
    channel_reserve.click()
    time.sleep(0.5)
    # 3. '통합예약조회' 메뉴 클릭
    integrated_reserve = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#menu_16 a")))
    integrated_reserve.click()
    time.sleep(0.5)

def click_channel_option(driver, wait):
    channel_select = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(channel_select)
    # 채널 선택 드롭다운 클릭
    channel_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='channelSeqnoBox']")))
    driver.execute_script("arguments[0].click();", channel_select)
    time.sleep(0.5)
    # 복지몰 선택
    welfare_mall_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='channelSeqArr2']")))
    welfare_mall_label.click()
    time.sleep(0.5)
    # [x] 선택
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_close")))
    close_button.click()
    time.sleep(0.5)

def click_search_reserve_detail(driver, wait):
    # 검색 버튼 클릭
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_search")))
    search_button.click()
    time.sleep(0.5)
    # 예약 상세 진입
    reserve_detail = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "table.tbl_list tbody tr td a")))
    reserve_detail.click()
    time.sleep(2)
    #iframe 탈출
    driver.switch_to.default_content()
    time.sleep(2)

# def switch_to_reservation_iframe(driver, wait):
#     try:
#         # iframe이 로드될 때까지 대기
#         wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
#         # 모든 iframe 요소를 가져옴
#         iframes = driver.find_elements(By.TAG_NAME, "iframe")
#         # print(f"찾은 iframe 개수: {len(iframes)}")
#         for index, iframe in enumerate(iframes):
#             src_attr = iframe.get_attribute("src")
#             class_attr = iframe.get_attribute("class")
#             # print(f"iframe {index} src: {src_attr}")
#             # print(f"iframe {index} 클래스: {class_attr}")
#         second_iframe = iframes[1]
#         # 두번째 iframe의 클래스로 접근
#         if len(iframes) >= 2:
#             second_iframe = iframes[1]
#             class_attr = second_iframe.get_attribute("class")
#             driver.switch_to.frame(second_iframe)
#             # print(f"두번째 iframe(class: {class_attr})으로 전환 완료")
#         else:
#             print("두번째 iframe을 찾지 못했습니다.")
#     except TimeoutException:
#         print("iframe 요소를 찾는 동안 타임아웃이 발생했습니다.")
#     except Exception as e:
#         print(f"iframe 전환 중 오류 발생: {e}")

def check_reservation_status(driver, wait):
    wait_reservation_element = driver.find_element(By.XPATH, "//*[@id=‘myTabbar’]/div/div/div[3]/div/iframe")
    driver.switch_to.frame(wait_reservation_element)
    # 셀렉트박스 클릭하여 옵션 리스트 열기
    wait_reservation_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'current') and text()='대기예약']")))
    wait_reservation_element.click()

    # '예약확정' 옵션 클릭
    reservation_confirm_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.option[data-value='10']")))
    reservation_confirm_option.click()
    time.sleep(0.5)
    #변경 버튼 선택
    change_button = wait.until(EC.element_to_be_clickable((By.ID, "saveResStatus")))
    change_button.click()
    time.sleep(0.5)
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

def finalize_reservation():
    driver, wait = setup_driver()
    
    some_function()

    try:
        manager_login(driver, wait)
    except Exception as e:
        print(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        channel_reserve_management(driver, wait)
    except Exception as e:
        print(f"채널 예약 관리 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        click_channel_option(driver, wait)
    except Exception as e:
        print(f"채널 옵션 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        click_search_reserve_detail(driver, wait)
    except Exception as e:
        print(f"예약 상세 검색 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # try:
    #     switch_to_reservation_iframe(driver, wait)
    # except Exception as e:
    #     print(f"예약 상세 페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    try:
        check_reservation_status(driver, wait)
    except Exception as e:
        print(f"예약 상태 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
        
    finally:
        driver.quit()

if __name__ == "__main__":
    finalize_reservation()
