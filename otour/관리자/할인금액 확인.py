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

def login(driver, wait):
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
    time.sleep(1)
    login_button.click()
    
    # 로그인 후 대기
    time.sleep(2)

def channel_reserve_management(driver, wait):
    # 1. '예약관리' 메뉴 클릭
    reserve_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_wrench")))
    reserve_menu.click()
    time.sleep(0.5)
    
    # 2. '채널관리' 서브메뉴 클릭
    channel_reserve = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '채널관리')]")))
    channel_reserve.click()
    time.sleep(0.5)
    
    # 3. '채널정보관리' 메뉴 클릭 
    integrated_reserve = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#menu_29 a")))
    integrated_reserve.click()
    time.sleep(3)  # iframe 로드를 위해 대기 시간 증가

def switch_to_target_iframe(driver, wait):
    try:
        # iframe이 로드될 때까지 대기
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        
        # 모든 iframe 요소를 가져옴
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        # print(f"찾은 iframe 개수: {len(iframes)}")
        
        for index, iframe in enumerate(iframes):
            src_attr = iframe.get_attribute("src")
            class_attr = iframe.get_attribute("class")
            # print(f"iframe {index} src: {src_attr}")
            # print(f"iframe {index} 클래스: {class_attr}")
            
        second_iframe = iframes[1]
        # 두번째 iframe의 클래스로 접근
        if len(iframes) >= 2:
            second_iframe = iframes[1]
            class_attr = second_iframe.get_attribute("class")
            driver.switch_to.frame(second_iframe)
            # print(f"두번째 iframe(class: {class_attr})으로 전환 완료")
        else:
            print("두번째 iframe을 찾지 못했습니다.")

    except TimeoutException:
        print("iframe 요소를 찾는 동안 타임아웃이 발생했습니다.")
        return False
    except Exception as e:
        print(f"iframe 전환 중 오류 발생: {e}")
        return False
    time.sleep(2)

def search_and_click_channel(driver, wait):
    # 채널명 하드코딩
    channel_name = "(주)이노풀"
    # 채널명 선택
    channel_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{channel_name}']")))
    channel_link.click()
    time.sleep(0.5)

def uncheck_discount_checkboxes(driver, wait):
    # 모든 할인 체크박스 요소를 가져옴
    discount_checkboxes = driver.find_elements(By.NAME, "discountChk")
    
    for checkbox in discount_checkboxes:
        # 체크박스가 선택되어 있는지 확인
        if checkbox.is_selected():
            # 선택되어 있으면 클릭하여 해제
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.5)
    click_button = wait.until(EC.element_to_be_clickable((By.ID, "channeledit")))
    click_button.click()
    time.sleep(0.5)

# 테스트 상품코드 입력
homepage_url = "https://devinp.hanabizwel.com/pages/overseas/package/detail/84698471/MO"

def homepage_login(driver, wait):
    # 새 탭 열기
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    # 메인 페이지 접속
    driver.get(homepage_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    # # 로그인 버튼 클릭
    # login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login']")))
    # login_link.click()
    # time.sleep(2)
    # # ID 입력  개발:otourtest / 운영:sbrr103
    # username = wait.until(EC.presence_of_element_located((By.ID, "idSet")))
    # username.clear()
    # username.send_keys("seohaqa")
    # # 비밀번호 입력  개발 : cjmall2$ / 운영 : cj011992???
    # password = wait.until(EC.presence_of_element_located((By.NAME, "passwordSet")))
    # password.clear()
    # password.send_keys("rhaoddl1143!")
    # # 로그인 버튼 클릭
    # login_button = wait.until(EC.element_to_be_clickable((By.ID, "memberLoginBtn")))
    # login_button.click()
    # time.sleep(2)
    # # 특정 URL 진입
    # driver.get(homepage_url)
    # wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # time.sleep(2)

# 금액 요소 찾기
def get_price(driver, wait):
    global price  # 함수 내부에서 전역 변수 선언
    price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3#totalAmount")))
    # 금액 텍스트 가져오기
    price_text = price_element.text
    # 금액을 정수로 변환
    price = int(price_text.replace(',', ''))
    return price

def switch_to_manager_page(driver, wait):
    # 이전 탭으로 전환
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.5)
    # 페이지 새로고침
    driver.refresh()
    time.sleep(2)
    channel_reserve_management(driver, wait)
    switch_to_target_iframe(driver, wait)
    search_and_click_channel(driver, wait)

def check_discount_checkboxes(driver, wait):
    # 모든 할인 체크박스 요소를 가져옴
    discount_checkboxes = driver.find_elements(By.NAME, "discountChk")
    
    for checkbox in discount_checkboxes:
        # 체크박스가 선택되어 있는지 확인
        if checkbox.is_selected():
            # 선택되어 있지 않으면 클릭하여 선택
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.5)
    click_button = wait.until(EC.element_to_be_clickable((By.ID, "channeledit")))
    click_button.click()
    time.sleep(0.5) 

# 다음 탭으로 전환
def switch_to_next_tab(driver, wait):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(0.5)
    driver.refresh()
    time.sleep(2)

def get_discount_amount(driver, wait):
    global discount_amount 
    discount_amount_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span#discountAmount")))
    discount_amount_text = discount_amount_element.text
    discount_amount = int(discount_amount_text.replace(',', ''))
    return discount_amount

def check_discount_amount(driver, wait):
    if discount_amount == price:
        print("할인금액 확인 완료")
    else:
        print("할인금액 확인 실패")
    pyautogui.confirm(title = 'complete', text = '테스트 완료')


def finalize_reservation():
    driver, wait = setup_driver()
    
    some_function()

    try:
        login(driver, wait)
        print("로그인 완료")
    except Exception as e:
        print(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        channel_reserve_management(driver, wait)
        print("채널 예약 관리 완료")
    except Exception as e:
        print(f"채널 예약 관리 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        switch_to_target_iframe(driver, wait)
        print("타켓 iframe 전환 완료")
    except Exception as e:
        print(f"타켓 iframe 전환 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        search_and_click_channel(driver, wait)
        print("채널명 클릭 완료")
    except Exception as e:
        print(f"채널명 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        uncheck_discount_checkboxes(driver, wait)
        print("할인 체크박스 해제 완료")
    except Exception as e:
        print(f"할인 체크박스 해제 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        homepage_login(driver, wait)
        print("홈페이지 전환 완료")
    except Exception as e:
        print(f"홈페이지 전환 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        get_price(driver, wait)
        print("금액 확인 완료")
    except Exception as e:
        print(f"금액 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        switch_to_manager_page(driver, wait)
        print("관리자 페이지 전환 완료")
    except Exception as e:
        print(f"관리자 페이지 전환 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        check_discount_checkboxes(driver, wait)
        print("체크박스 선택 완료")
    except Exception as e:
        print(f"체크박스 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        switch_to_next_tab(driver, wait)
        print("다음 탭으로 전환 완료")
    except Exception as e:
        print(f"다음 탭으로 전환 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        get_discount_amount(driver, wait)
        print("할인금액 확인 완료")
    except Exception as e:
        print(f"할인금액 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        check_discount_amount(driver, wait)
        print("할인금액 확인 완료")
    except Exception as e:
        print(f"할인금액 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    
    finally:
        driver.quit()

if __name__ == "__main__":
    finalize_reservation()
