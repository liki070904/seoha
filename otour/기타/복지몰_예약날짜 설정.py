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
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

# 테스트 상품코드 입력
homepage_url = "https://devwel.hanabizwel.com"
# driver.get("https://wel.hanabizwel.com/")   #운영
html = urlopen(homepage_url)
soup = BeautifulSoup(html, "html.parser")

def login(driver, wait):
    driver.get(homepage_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    # 로그인 버튼 클릭
    login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login']")))
    login_link.click()
    time.sleep(2)
    # ID 입력  개발:otourtest / 운영:sbrr103   /   포스코이앤씨 : seoha
    username = wait.until(EC.presence_of_element_located((By.ID, "idSet")))
    username.clear()
    username.send_keys("seohaqa")
    # 비밀번호 입력  개발 : cjmall2$ / 운영 : cj011992???
    password = wait.until(EC.presence_of_element_located((By.NAME, "passwordSet")))
    password.clear()
    password.send_keys("rhaoddl1143!")
    time.sleep(1)
    # 로그인 버튼 클릭
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "memberLoginBtn")))
    login_button.click()
    time.sleep(1)

def navigate_to_package(driver, wait):
    # 패키지 클릭
    overseas_package = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='javascript:void(0)']")))
    overseas_package.click()
    time.sleep(1)
    # 동남아/대만/서남아 패키지 클릭
    southeast_asia = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[rel='menu1_1']")))
    southeast_asia.click()
    time.sleep(1)
    # 푸켓/끄라비 패키지 클릭
    phuket = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/pages/overseas/package/list/v/package/HKT/KBV']")))
    phuket.click()
    time.sleep(1)

# def navigate_to_golf(driver, wait):
#     # 해외골프 클릭
#     overseas_golf = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='해외골프']")))
#     overseas_golf.click()
#     time.sleep(1)
#     # 골프_동남아 클릭
#     golf_southeast_asia = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='동남아']")))
#     golf_southeast_asia.click()
#     time.sleep(1)
#     # 방콕/파타야 클릭
#     bangkok = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/pages/overseas/package/list/v/golf/BKK/PYX']")))
#     bangkok.click()
#     time.sleep(1)

def select_supplier(driver, wait):
    # 한진 : HJ / 롯데 : LO / 하나 : HN / 모두 : MO
    supplier_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='MO']")))
    driver.execute_script("arguments[0].click();", supplier_checkbox)
    time.sleep(1)

def select_product(driver, wait):
    product_index = 1
    while product_index <= 5:
        try:
            # 상품의 '상세보기' 버튼 클릭
            detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='product_list']/li[{product_index}]/div[1]/div[2]/div[3]/button")))
            driver.execute_script("arguments[0].scrollIntoView(true);", detail_button)
            driver.execute_script("arguments[0].click();", detail_button)
            print(f"{product_index}번째 상품 상세보기 버튼 클릭 완료")
            time.sleep(1)
        except TimeoutException:
            logging.error(f"상품 {product_index}의 '상세보기' 버튼을 찾을 수 없습니다.")
            continue
        try:
            for _ in range(3):  # 달력 다음 달 버튼 3번 클릭
                button = driver.find_element(By.CSS_SELECTOR, "button.btn_arrow.next.monthnext")
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                driver.execute_script("arguments[0].click();", button)  # JavaScript로 클릭
                time.sleep(0.5)
                # 팝업이 있다면 확인 버튼 클릭
                popup = driver.find_elements(By.CLASS_NAME, "swal2-confirm")
                if popup:
                    popup[0].click()
                    time.sleep(0.5)
            # 선택 가능한 가격 있는 날짜가 있는 경우
            available_dates = driver.find_elements(By.CSS_SELECTOR, "div.price.lowest")
            if available_dates:
                print("선택 가능한 가격 있는 날짜가 있습니다.")
                available_dates[0].click()  # 첫 번째 가능한 날짜 선택
                time.sleep(1)
                # 첫 번째 상품의 '자세히보기' 버튼 클릭
                detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='자세히보기']")))
                driver.execute_script("arguments[0].click();", detail_button)
                time.sleep(1)   
                break
            else:       
                # 검색 조건에 해당하는 상품이 없는 경우 확인
                no_search_result = driver.find_elements(By.CSS_SELECTOR, "li.box.no_srch")
                if no_search_result:
                    print("검색 조건에 해당하는 상품이 없습니다.")
                    # 다음 상품으로 이동하기 위해 현재 상품의 상세보기 창 닫기
                    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.fill_cool_grey90.view_more_btn.active")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
                    driver.execute_script("arguments[0].click();", close_button)
                    product_index += 1
                    time.sleep(0.5)
                    continue
                
        except TimeoutException:
            logging.error(f"상품 {product_index}의 달력 버튼을 찾을 수 없습니다.")
            continue
    

def switch_to_reservation(driver, wait):
    # 현재 윈도우 핸들 저장
    original_window = driver.current_window_handle
    wait.until(EC.number_of_windows_to_be(2))
    # 새 윈도우 핸들 찾기
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(2)
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

def test_web_application():
    driver, wait = setup_driver()
    
    some_function()

    try:
        login(driver, wait)
        print("로그인 완료")
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 패키지 선택
        navigate_to_package(driver, wait)
        print("패키지 선택 완료")
    except Exception as e:
        logging.error(f"패키지 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # try:
    #     # 골프 선택
    #     navigate_to_golf(driver, wait)
    # except Exception as e:
    #     logging.error(f"골프 선택 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    try:
        # 공급사 선택
        select_supplier(driver, wait)
        print("공급사 선택 완료")
    except Exception as e:
        logging.error(f"공급사 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 상품 선택
        select_product(driver, wait)
        print("상품 선택 완료")
    except Exception as e:
        logging.error(f"상품 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약 페이지 이동
        switch_to_reservation(driver, wait)
        print("예약 페이지 이동 완료")
    except Exception as e:
        logging.error(f"예약 페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    finally:
        driver.quit()

if __name__ == "__main__":
    test_web_application()