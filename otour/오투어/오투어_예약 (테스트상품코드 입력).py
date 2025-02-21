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
homepage_url = "https://devotour.cjonstyle.com/pages/overseas/package/detail/OP20250221187/HJ"
    # driver.get("https://devotour.cjonstyle.com/pages/overseas/package/detail/OP20250111537/HJ")
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
    # ID 입력  개발:otourtest / 운영:sbrr103
    username = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='id_input']")))
    username.clear()
    username.send_keys("otourtest")
    # 비밀번호 입력  개발 : cjmall2$ / 운영 : cj011992???
    password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='password_input']")))
    password.clear()
    password.send_keys("cjmall2$")
    # 로그인 버튼 클릭
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginSubmit']")))
    login_button.click()
    time.sleep(1)
    # 특정 URL 진입
    driver.get(homepage_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)

# def navigate_to_package(driver, wait):
    # # 오투어 패키지 클릭
    # overseas_package = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='javascript:void(0)']")))
    # overseas_package.click()
    # time.sleep(1)
    
    # # 동남아/대만/서남아 패키지 클릭
    # southeast_asia = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[rel='menu1_1']")))
    # southeast_asia.click()
    # time.sleep(1)
    
    # # 푸켓/끄라비 패키지 클릭
    # phuket = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/pages/overseas/package/list/v/package/HKT/KBV']")))
    # phuket.click()
    # time.sleep(1)

# def navigate_to_golf(driver, wait):
#     # 오투어 해외골프 클릭
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


# def select_supplier(driver, wait):
#     # 한진 : HJ / 롯데 : LO / 하나 : HN / 모두 : MO
#     hanjin_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='MO']")))
#     driver.execute_script("arguments[0].click();", hanjin_checkbox)
#     time.sleep(1)

# def select_product(driver, wait):
#     product_index = 1
#     while product_index <= 5:
#         try:
#             # 상품의 '상세보기' 버튼 클릭
#             detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='product_list']/li[{product_index}]/div[1]/div[2]/div[3]/button")))
#             driver.execute_script("arguments[0].scrollIntoView(true);", detail_button)
#             driver.execute_script("arguments[0].click();", detail_button)
#             print(f"{product_index}번째 상품 상세보기 버튼 클릭 완료")
#             time.sleep(1)
#         except TimeoutException:
#             logging.error(f"상품 {product_index}의 '상세보기' 버튼을 찾을 수 없습니다.")
#             continue
#         try:
#             for _ in range(3):  # 달력 다음 달 버튼 3번 클릭
#                 button = driver.find_element(By.CSS_SELECTOR, "button.btn_arrow.next.monthnext")
#                 driver.execute_script("arguments[0].scrollIntoView(true);", button)
#                 driver.execute_script("arguments[0].click();", button)  # JavaScript로 클릭
#                 time.sleep(0.5)
#                 # 팝업이 있다면 확인 버튼 클릭
#                 popup = driver.find_elements(By.CLASS_NAME, "swal2-confirm")
#                 if popup:
#                     popup[0].click()
#                     time.sleep(0.5)
#             # 선택 가능한 가격 있는 날짜가 있는 경우
#             available_dates = driver.find_elements(By.CSS_SELECTOR, "div.price.lowest")
#             if available_dates:
#                 print("선택 가능한 가격 있는 날짜가 있습니다.")
#                 available_dates[0].click()  # 첫 번째 가능한 날짜 선택
#                 time.sleep(1)
#                 # 첫 번째 상품의 '자세히보기' 버튼 클릭
#                 detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='자세히보기']")))
#                 driver.execute_script("arguments[0].click();", detail_button)
#                 time.sleep(1)   
#                 break
#             else:       
#                 # 검색 조건에 해당하는 상품이 없는 경우 확인
#                 no_search_result = driver.find_elements(By.CSS_SELECTOR, "li.box.no_srch")
#                 if no_search_result:
#                     print("검색 조건에 해당하는 상품이 없습니다.")
#                     # 다음 상품으로 이동하기 위해 현재 상품의 상세보기 창 닫기
#                     close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.fill_cool_grey90.view_more_btn.active")))
#                     driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
#                     driver.execute_script("arguments[0].click();", close_button)
#                     product_index += 1
#                     time.sleep(0.5)
#                     continue
                
#         except TimeoutException:
#             logging.error(f"상품 {product_index}의 달력 버튼을 찾을 수 없습니다.")
#             continue        
            
# def switch_to_reservation(driver, wait):
#     # 현재 윈도우 핸들 저장
#     original_window = driver.current_window_handle
#     wait.until(EC.number_of_windows_to_be(2))
    
#     # 새 윈도우 핸들 찾기
#     for window_handle in driver.window_handles:
#         if window_handle != original_window:
#             driver.switch_to.window(window_handle)
#             break
#     time.sleep(2)
    
def fill_reservation_form(driver, wait):
    # 예약하기 버튼 클릭
    reserve_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='btnreservation']")))
    driver.execute_script("arguments[0].click();", reserve_button)
    time.sleep(1)

    # 예약 옵션 체크박스 찾기 및 클릭
    checkboxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][value='Y']")))
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.5)

def input_traveler_info(driver, wait):            
    # 이름 입력
    name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#user")))
    name_input.send_keys("테스트")
    
    # 생년월일 입력
    birth_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#dateOfBirth")))
    birth_input.send_keys("19880728")
    
    # 이메일 입력
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#email")))
    email_input.send_keys("seoha.lee@ntoday.kr")
    
    # 전화번호 입력
    phone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#phNm")))
    phone_input.send_keys("01022077353")
    
    # 동일인 체크박스 클릭
    same_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#same1")))
    driver.execute_script("arguments[0].click();", same_checkbox)
    
    # 성별 여성 선택
    female_radio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#femaleA_1")))
    driver.execute_script("arguments[0].click();", female_radio)
    
    # 영문 성 입력
    eng_lastname = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#tEnSuNm1")))
    eng_lastname.send_keys("LEE")
    
    # 영문 이름 입력
    eng_firstname = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#tEnNm1")))
    eng_firstname.send_keys("SEOHA")

def complete_reservation(driver, wait):
    # 예약 버튼 클릭
    reserve_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a#btnbook.btn.btn_lg.fill_primary.w100p")))
    driver.execute_script("arguments[0].click();", reserve_button)
    time.sleep(10)

def check_reservation_status(driver, wait):
    # 예약내역 확인 버튼 클릭
    check_reservation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn_reser")))
    driver.execute_script("arguments[0].click();", check_reservation)
    time.sleep(2)

def navigate_to_reservation_list(driver, wait):
    # 예약리스트 바로가기 버튼 클릭
    check_reservation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/welfareMall/mypage/main']")))
    driver.execute_script("arguments[0].click();", check_reservation)
    pyautogui.confirm(title = 'complete', text = '테스트 완료')
    time.sleep(2)


def test_web_application():
    driver, wait = setup_driver()
    
    try:
        login(driver, wait)
    except Exception as e:
        print(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # try:
    #     # 패키지 선택
    #     navigate_to_package(driver, wait)
    # except Exception as e:
    #     print(f"패키지 선택 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    # try:
    #     # 골프 선택
    #     navigate_to_golf(driver, wait)
    # except Exception as e:
    #     print(f"골프 선택 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    # try:
    #     # 공급사 선택
    #     select_supplier(driver, wait)
    # except Exception as e:
    #     print(f"공급사 선택 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    # try:
    #     # 상품 선택
    #     select_product(driver, wait)
    # except Exception as e:
    #     print(f"상품 선택 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    # try:
    #     # 예약 페이지 이동
    #     switch_to_reservation(driver, wait)
    # except Exception as e:
    #     print(f"예약 페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    try:
        # 예약 양식 입력
        fill_reservation_form(driver, wait)
    except Exception as e:
        print(f"예약 양식 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 여행자 정보 입력
        input_traveler_info(driver, wait)
    except Exception as e:
        print(f"여행자 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약 완료
        complete_reservation(driver, wait)
    except Exception as e:
        print(f"예약 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약내역 확인
        check_reservation_status(driver, wait)
    except Exception as e:
        print(f"예약내역 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약리스트 이동
        navigate_to_reservation_list(driver, wait)
    except Exception as e:
        print(f"예약리스트 이동 테스트 중 오류가 발생했습니다: {str(e)}")
        return
  
    finally:
        driver.quit()

if __name__ == "__main__":
    test_web_application()
