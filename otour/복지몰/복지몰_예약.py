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

# 관리자 홈페이지 입력
homepage_url = "https://devwel.hanabizwel.com"
# driver.get("https://wel.hanabizwel.com/")   #운영
# 관리자 URL
admin_url = "https://devfss.hanatourbiz.com/login"

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
    time.sleep(1)
    
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
    time.sleep(1)

def check_reservation(driver, wait):
    # 예약내역 확인 버튼 클릭
    check_reservation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn_reser")))
    driver.execute_script("arguments[0].click();", check_reservation)
    time.sleep(1)

def navigate_to_reservation_list(driver, wait):
    # 예약리스트 바로가기 버튼 클릭
    check_reservation_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/welfareMall/mypage/main']")))
    driver.execute_script("arguments[0].click();", check_reservation_list)
    time.sleep(1)

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
    # 복지몰 선택 (오투어 : channelSeqArr1 / 복지몰 : channelSeqArr2 / 삼성전기 : channelSeqArr10)
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
    # 셀렉트박스 클릭하여 옵션 리스트 열기
    wait_reservation_element = driver.find_element(By.XPATH, "//*[@id=‘myTabbar’]/div/div/div[3]/div/iframe")
    driver.switch_to.frame(wait_reservation_element)
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

def process_payment(driver, wait):
    # 이전 탭으로 전환
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.5)
    # 페이지 새로고침
    driver.refresh()
    time.sleep(2)
    # 첫 번째 결제하기 버튼 찾기 및 클릭
    payment_btn = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.line_primary.btnpayment")))
    payment_btn[0].click()
    time.sleep(1)

def complete_payment(driver, wait):
    # 전액사용 버튼 클릭
    inquire_point_btn = wait.until(EC.element_to_be_clickable((By.ID, "inquirePoint")))
    driver.execute_script("arguments[0].click();", inquire_point_btn)
    time.sleep(1)
    # 결제하기 버튼 클릭
    payment_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnpayment")))
    driver.execute_script("arguments[0].click();", payment_btn)
    time.sleep(1)
    # 결제 확인 팝업의 확인 버튼 클릭
    confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnConfirm01")))
    driver.execute_script("arguments[0].click();", confirm_btn)
    time.sleep(1)

def click_my_travel(driver, wait):
    # 마이페이지 이동
    my_travel_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='mypage']")))
    my_travel_link.click()
    print("마이페이지 이동 완료")
    pyautogui.confirm(title = 'complete', text = '테스트 완료')
    time.sleep(10)

def test_web_application():
    driver, wait = setup_driver()
    
    some_function()

    try:
        login(driver, wait)
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 패키지 선택
        navigate_to_package(driver, wait)
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
    except Exception as e:
        logging.error(f"공급사 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 상품 선택
        select_product(driver, wait)
    except Exception as e:
        logging.error(f"상품 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약 페이지 이동
        switch_to_reservation(driver, wait)
    except Exception as e:
        logging.error(f"예약 페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약 양식 입력
        fill_reservation_form(driver, wait)
    except Exception as e:
        logging.error(f"예약 양식 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 여행자 정보 입력
        input_traveler_info(driver, wait)
    except Exception as e:
        logging.error(f"여행자 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약 완료
        complete_reservation(driver, wait)
    except Exception as e:
        logging.error(f"예약 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약내역 확인
        check_reservation(driver, wait)
    except Exception as e:
        logging.error(f"예약내역 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        # 예약리스트 이동
        navigate_to_reservation_list(driver, wait)
    except Exception as e:
        logging.error(f"예약리스트 이동 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        manager_login(driver, wait)
    except Exception as e:
        logging.error(f"관리자 로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        channel_reserve_management(driver, wait)
    except Exception as e:
        logging.error(f"채널 예약 관리 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        click_channel_option(driver, wait)
    except Exception as e:
        logging.error(f"채널 옵션 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        click_search_reserve_detail(driver, wait)
    except Exception as e:
        logging.error(f"예약 상세 검색 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # try:
    #     switch_to_reservation_iframe(driver, wait)
    # except Exception as e:
    #     logging.error(f"예약 상세 페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
    #     return
    try:
        check_reservation_status(driver, wait)
    except Exception as e:
        logging.error(f"예약 상태 확인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        process_payment(driver, wait)
    except Exception as e:
        logging.error(f"결제 처리 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        complete_payment(driver, wait)
    except Exception as e:
        logging.error(f"결제 완료 과정 중 오류 발생: {str(e)}")
        return
    try:
        click_my_travel(driver, wait)
    except Exception as e:
        logging.error(f"결제 상태 확인 중 오류 발생: {str(e)}")
        return
    finally:
        driver.quit()

if __name__ == "__main__":
    test_web_application()
