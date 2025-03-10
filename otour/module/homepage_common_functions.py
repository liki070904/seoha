from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from otour.module.setup_common_functions import (click)
import logging, time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# 복지몰 URL
dev_wel_homepage_url = "https://devwel.hanabizwel.com"
wel_homepage_url = "https://wel.hanabizwel.com"
# 오투어 URL
dev_otour_homepage_url = "https://devotour.cjonstyle.com/"
otour_homepage_url = "https://otour.cjonstyle.com/"
# 오투어 상품코드 URL
otour_product_homepage_url = "https://devotour.cjonstyle.com/pages/overseas/package/detail/OP20250221187/HJ"
# 복지몰 상품코드 URL
wel_product_homepage_url = "https://devwel.hanabizwel.com/pages/overseas/package/detail/OP20250613772/HJ"

# 복지몰 오픈
def wel_homepage_open(driver, wait):
    try:
        driver.get(wel_homepage_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("복지몰 페이지 열기 성공")
    except Exception as e:
        logging.error(f"복지몰 페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")
# 오투어 오픈
def otour_homepage_open(driver, wait):
    try:
        driver.get(dev_otour_homepage_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("오투어 페이지 열기 성공")
    except Exception as e:
        logging.error(f"복지몰 페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")
# 오투어 상품코드 오픈
def otour_product_homepage_open(driver, wait):
    try:
        driver.get(otour_product_homepage_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("오투어 페이지 열기 성공")
    except Exception as e:
        logging.error(f"복지몰 페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")
# 복지몰 상품코드 오픈
def wel_product_homepage_open(driver, wait):
    try:
        driver.get(wel_product_homepage_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("오투어 페이지 열기 성공")
    except Exception as e:
        logging.error(f"복지몰 페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")
# 복지몰 로그인
def wel_login(driver, wait, user_id, user_pw):
    try:
        # 로그인 버튼 클릭
        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login']")))
        click(driver, login_link)
        time.sleep(1)
        # ID 입력  개발:otourtest / 운영:sbrr103   /   포스코이앤씨 : seoha
        driver.find_element(By.ID, "idSet").send_keys(user_id)
        driver.find_element(By.ID, "passwordSet").send_keys(user_pw)
        # 로그인 버튼 클릭
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "memberLoginBtn")))
        click(driver, login_button)
        logger.info("로그인 성공")
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    time.sleep(1)
# 오투어 로그인
def otour_login(driver, wait, user_id, user_pw):
    try:
        # 로그인 버튼 클릭
        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login']")))
        click(driver, login_link)
        time.sleep(1)
        # ID 입력  개발:otourtest / 운영:sbrr103   /   포스코이앤씨 : seoha
        driver.find_element(By.XPATH, "//*[@id='id_input']").send_keys(user_id)
        driver.find_element(By.XPATH, "//*[@id='password_input']").send_keys(user_pw)
        # 로그인 버튼 클릭
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginSubmit']")))
        click(driver, login_button)
        logger.info("로그인 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 패키지 클릭
def travel_products_package(driver, wait, travel_products, travel_city, travel_area):
    try:
        # 1depth 클릭
        travel_products = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{travel_products}']")))
        travel_products.click()

        # 2depth 클릭
        travel_city = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{travel_city}']")))
        travel_city.click()

        # 3depth 클릭
        travel_area = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{travel_area}']")))
        travel_area.click()

        logger.info("패키지 클릭 성공")
    except Exception as e:
        logging.error(f"패키지 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 국내숙박 클릭
def travel_products_domestic(driver, wait):
    try:
        # 1depth 클릭
        travel_products = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='국내숙박']")))
        click(driver,travel_products)
        time.sleep(1)
        logger.info("국내숙박 클릭 성공")
    except Exception as e:
        logging.error(f"패키지 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 낮은 가격순 필터
def low_price(driver, wait):
    try:
        time.sleep(1)
        lower_price = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div/div[1]/div[3]/div[2]/div[1]/label')))
        click(driver,lower_price)
        logger.info("낮은 가격순 필터 클릭 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"낮은 가격순 필터 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 국내숙박 결제용 상품 선택
def click_product(driver, wait):
    try:
        time.sleep(1)
        product = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div/div[1]/div[4]/div[2]/div[1]/ul/li[1]/div/div[2]/div[3]/div[2]/a[2]')))
        click(driver, product)
        logger.info("국내숙박 결제용 상품 선택 성공")
    except Exception as e:
        logging.error(f"국내숙박 결제용 상품 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 날짜 변경
def change_date(driver, wait):
    try:
        click_datepicker = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_litepicker"]')))
        click(driver, click_datepicker)
        time.sleep(1)
        # 모든 날짜 요소 가져오기
        dates = driver.find_elements(By.XPATH, '//*[@id="sub_rangeContainer"]/div/div/div/div[2]/div[3]//div[contains(@class, "day-item")]')
        # 마지막 두 개의 날짜 요소 선택
        if len(dates) >= 2:
            check_in_date = dates[-2]  # 마지막에서 두 번째 날짜 (첫 번째 선택할 날짜)
            click(driver, check_in_date)  # 첫 번째 날짜 클릭
            time.sleep(1)
            dates = driver.find_elements(By.XPATH, '//*[@id="sub_rangeContainer"]/div/div/div/div[2]/div[3]//div[contains(@class, "day-item")]')
            check_out_date = dates[-1]  # 마지막 날짜 (두 번째 선택할 날짜)
            click(driver, check_out_date)  # 두 번째 날짜 클릭
            time.sleep(1)
        click_date = driver.find_element(By.XPATH, '//*[@id="sub_datePop2"]/div[2]/div/div[2]/button')
        click(driver, click_date)
        search_room = driver.find_element(By.XPATH, '//*[@id="sub_btnsearch"]')
        click(driver, search_room)
        time.sleep(1)
        logger.info("날짜변경 성공")
    except Exception as e:
        logging.error(f"날짜변경 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 즉시결제 선택
def immediate_payment(driver, wait):
    try:
        click_pay = driver.find_element(By.XPATH, '//*[@id="47122"]')
        click(driver, click_pay)
        popup_click = driver.find_element(By.XPATH, '/html/body/div[8]/div/div[6]/button[1]')
        click(driver, popup_click)
        time.sleep(2)
        logger.info("즉시결제 선택 성공")
    except Exception as e:
        logging.error(f"즉시결제 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약자 정보 입력
def reservation_info(driver, wait, name_input, birth_input, email_input, phone_input):
    try:
        # 이름 입력
        driver.find_element(By.ID, "user").send_keys(name_input)
        # 생년월일 입력
        driver.find_element(By.ID, "dateOfBirth").send_keys(birth_input)
        # 이메일 입력
        driver.find_element(By.ID, "email").send_keys(email_input)
        # 전화번호 입력
        driver.find_element(By.ID, "phNm").send_keys(phone_input)
        logger.info("예약자 정보 입력 성공")
    except Exception as e:
        logging.error(f"예약자 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
# 트윈 옵션 추가 & 메모 입력
def add_twin_option(driver, wait, memo):
    try:
        add_option = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div[2]/div[1]/div[3]/div[2]/div/div/div[2]/button[2]')
        click(driver, add_option)
        logger.info("옵션 추가 성공")
        driver.find_element(By.ID, "applyMemo").send_keys(memo)
        logger.info("메모 추가 성공")
    except Exception as e:
        logging.error(f"옵션 추가 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 약관 동의
def agree_conditions(driver, wait):
    try:
        all_agree = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div/label')
        click(driver, all_agree)
        first_condition = driver.find_element(By.XPATH, '//*[@id="agreePop1"]/div[2]/div[3]/div/button[1]')
        click(driver, first_condition)
        second_condition = driver.find_element(By.XPATH, '//*[@id="agreePop2"]/div[2]/div[3]/div/button[1]')
        click(driver, second_condition)
        third_condition = driver.find_element(By.XPATH, '//*[@id="agreePop3"]/div[2]/div[3]/div/button[1]')
        click(driver, third_condition)
        fourth_condition = driver.find_element(By.XPATH, '//*[@id="agreePop4"]/div[2]/div[3]/div/button[1]')
        click(driver, fourth_condition)
        fifth_condition = driver.find_element(By.XPATH, '//*[@id="agreePop5"]/div[2]/div[3]/div/button[1]')
        click(driver, fifth_condition)
        logger.info("약관 동의 성공")
    except Exception as e:
        logging.error(f"약관 동의 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 포인트 사용
def point_pay(driver, wait):
    try:
        all_point_pay = driver.find_element(By.XPATH, '//*[@id="inquirePoint"]')
        click(driver,all_point_pay)
        logger.info("포인트 전액 사용 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"포인트 전액 사용 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 결제하기 선택
def click_payment(driver, wait):
    try:
        payment = driver.find_element(By.XPATH, '//*[@id="btnbook"]')
        click(driver, payment)
        payment_popup = driver.find_element(By.XPATH, '/html/body/div[12]/div/div[6]/button[1]')
        click(driver, payment_popup)
        time.sleep(2)
        logger.info("포인트로 결제하기 성공")
    except Exception as e:
        logging.error(f"포인트로 결제하기 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 공급사 태그 클릭  한진 : HJ / 롯데 : LO / 하나 : HN / 모두 : MO
def select_supplier(driver, wait, value):
    try:
        supplier_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@value="{value}"]')))
        click(driver, supplier_checkbox)
        time.sleep(1)
        logger.info("공급사 선택 성공")
    except Exception as e:
        logging.error(f"공급사 선택 테스트 중 오류가 발생했습니다: {str(e)}")
# 상품 선택
def select_product(driver, wait):
    try:
        product_index = 1
        while product_index <= 5:
            try:
                # 상품의 '상세보기' 버튼 클릭
                detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='product_list']/li[{product_index}]/div[1]/div[2]/div[3]/button")))
                driver.execute_script("arguments[0].scrollIntoView(true);", detail_button)
                click(driver, detail_button)
                print(f"{product_index}번째 상품 상세보기 버튼 클릭 완료")
                time.sleep(1)
            except TimeoutException:
                logging.error(f"상품 {product_index}의 '상세보기' 버튼을 찾을 수 없습니다.")
                continue
            try:
                for _ in range(3):  # 달력 다음 달 버튼 3번 클릭
                    button = driver.find_element(By.CSS_SELECTOR, "button.btn_arrow.next.monthnext")
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    click(driver, button)
                    time.sleep(0.5)
                    # 팝업이 있다면 확인 버튼 클릭
                    popup = driver.find_elements(By.CLASS_NAME, "swal2-confirm")
                    if popup:
                        click(driver, popup[0])
                        time.sleep(0.5)
                # 선택 가능한 가격 있는 날짜가 있는 경우
                available_dates = driver.find_elements(By.CSS_SELECTOR, "div.price.lowest")
                if available_dates:
                    print("선택 가능한 가격 있는 날짜가 있습니다.")
                    click(driver, available_dates[0])  # 첫 번째 가능한 날짜 선택
                    time.sleep(1)
                    # 첫 번째 상품의 '자세히보기' 버튼 클릭
                    detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='자세히보기']")))
                    click(driver, detail_button)
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
                        click(driver, close_button)
                        product_index += 1
                        time.sleep(0.5)
                        continue

            except TimeoutException:
                logging.error(f"상품 {product_index}의 달력 버튼을 찾을 수 없습니다.")
                continue
        logger.info("상품 선택 성공")
    except Exception as e:
        logging.error(f"상품 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약하기 버튼 클릭
def fill_reservation_form(driver, wait):
    try:
        reserve_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='btnreservation']")))
        click(driver, reserve_button)
        time.sleep(1)
        agree_checkbox = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div')
        click(driver, agree_checkbox)
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)
        logger.info("예약하기 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"예약하기 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
# 성인 정보 입력
def input_traveler_info(driver, wait, name_input, birth_input, email_input, phone_input, eng_lastname, eng_firstname):
    try:
        # 이름 입력
        driver.find_element(By.ID, "input#user").send_keys(name_input)
        # 생년월일 입력
        driver.find_element(By.ID, "input#dateOfBirth").send_keys(birth_input)
        # 이메일 입력
        driver.find_element(By.ID, "input#email").send_keys(email_input)
        # 전화번호 입력
        driver.find_element(By.ID, "input#phNm").send_keys(phone_input)
        # 동일인 체크박스 클릭
        same_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#same1")))
        driver.execute_script("arguments[0].click();", same_checkbox)
        # 성별 여성 선택
        female_radio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#femaleA_1")))
        driver.execute_script("arguments[0].click();", female_radio)
        # 영문 성 입력
        driver.find_element(By.ID, "input#tEnSuNm1").send_keys(eng_lastname)
        # 영문 이름 입력
        driver.find_element(By.ID, "input#tEnNm1").send_keys(eng_firstname)
        logger.info("성인 정보 입력 성공")
    except Exception as e:
        logging.error(f"성인 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 아동 정보 입력
def input_traveler_info2(driver, wait, name_input, birth_input, eng_lastname, eng_firstname):
    try:
        driver.find_element(By.CSS_SELECTOR, "#orderCnt2Area input[name='tUser']").send_keys(name_input)
        # name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt2Area input[name='tUser']")))
        # name_input.send_keys("테스트아동")
        driver.find_element(By.CSS_SELECTOR, "#orderCnt2Area input[name='tDateOfBirth']").send_keys(birth_input)
        # birth_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt2Area input[name='tDateOfBirth']")))
        # birth_input.send_keys("20150101")
        male_radio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt2Area input#maleB_1")))
        click(driver, male_radio)
        driver.find_element(By.CSS_SELECTOR, "#orderCnt2Area input[name='tEnSuNm']").send_keys(eng_lastname)
        # eng_lastname = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt2Area input[name='tEnSuNm']")))
        # eng_lastname.send_keys("LEE")
        driver.find_element(By.CSS_SELECTOR, "#orderCnt2Area input[name='tEnNm']").send_keys(eng_firstname)
        # eng_firstname = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt2Area input[name='tEnNm']")))
        # eng_firstname.send_keys("SEOHA")
        time.sleep(0.5)
        logger.info("아동 정보 입력 성공")
    except Exception as e:
        logging.error(f"아동 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 유아 정보 입력
def input_traveler_info3(driver, wait, name_input, birth_input, eng_lastname, eng_firstname):
    try:
        driver.find_element(By.CSS_SELECTOR, "#orderCnt3Area input[name='tUser']").send_keys(name_input)
        # name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#orderCnt3Area input[name='tUser']")))
        # name_input.send_keys("테스트유아")
        driver.find_element(By.CSS_SELECTOR, "#orderCnt3Area input[name='tDateOfBirth']").send_keys(birth_input)
        # birth_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#orderCnt3Area input[name='tDateOfBirth']")))
        # birth_input.send_keys("20240101")
        female_radio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#orderCnt3Area input#femaleI_1")))
        click(driver, female_radio)
        driver.find_element(By.XPATH, "//*[@id='orderCnt3Area']/div/div[2]/dl[5]/dd/div/input").send_keys(eng_lastname)
        # eng_lastname = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='orderCnt3Area']/div/div[2]/dl[5]/dd/div/input")))
        # eng_lastname.send_keys("LEE")
        driver.find_element(By.XPATH, "//*[@id='orderCnt3Area']/div/div[2]/dl[6]/dd/div/input").send_keys(eng_firstname)
        # eng_firstname = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='orderCnt3Area']/div/div[2]/dl[6]/dd/div/input")))
        # eng_firstname.send_keys("SEOHA")
        time.sleep(0.5)
        logger.info("유아 정보 입력 성공")
    except Exception as e:
        logging.error(f"유아 정보 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약 버튼 클릭
def complete_reservation(driver, wait):
    try:
        reserve_complete_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a#btnbook.btn.btn_lg.fill_primary.w100p")))
        click(driver, reserve_complete_button)
        time.sleep(1)
        logger.info("예약 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"예약 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약내역 확인 버튼 클릭
def check_reservation(driver, wait):
    try:
        click_reservation = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='container']/div/div/div/div[2]/div[2]/div[5]/a[2]")))
        click(driver, click_reservation)
        time.sleep(1)
        logger.info("예약내역 확인 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"예약내역 확인 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약리스트 바로가기 버튼 클릭
def navigate_to_reservation_list(driver, wait):
    try:
        reservation_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div/div/div[2]/div[2]/div[6]/a')))
        click(driver, reservation_list)
        time.sleep(1)
        logger.info("예약리스트 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"예약리스트 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 금액 요소 찾기
def get_price(driver, wait):
    try:
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3#totalAmount")))
        price_text = price_element.text.strip()
        logger.info(f"금액 : {price_text}")
        return int(price_text.replace(',', ''))
    except Exception as e:
        logging.error(f"금액을 찾을 수 없습니다: {str(e)}")
        return
# 상품상세 > 예약 인원 추가
def add_reservation_person(driver, wait, adult_count=0, child_count=0, infant_count=0):
    try:
        # 성인 인원 추가
        for _ in range(adult_count):
            add_adult_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_count.plus.plus1")))
            click(driver, add_adult_button)
            time.sleep(0.5)
        # 아동 인원 추가
        for _ in range(child_count):
            add_child_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_count.plus.plus2.orderCnt2Plus")))
            click(driver, add_child_button)
            time.sleep(0.5)
        # 유아 인원 추가
        for _ in range(infant_count):
            add_infant_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_count.plus.plus2.orderCnt3Plus")))
            click(driver, add_infant_button)
            time.sleep(0.5)

        price = get_price(driver, wait)
        logger.info(f"성인: {adult_count}, 아동: {child_count}, 유아: {infant_count} 추가 성공")
        return price
    except Exception as e:
        logging.error(f"예약 인원 추가 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 결제하기 선택
def process_payment(driver, wait):
    try:
        # 첫 번째 결제하기 버튼 찾기 및 클릭
        payment_btn = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.line_primary.btnpayment")))
        click(driver, payment_btn[0])
        time.sleep(1)
        logger.info("결제하기 선택 성공")
    except Exception as e:
        logging.error(f"결제하기 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 포인트 결제
def complete_payment(driver, wait):
    try:
        # 전액사용 버튼 클릭
        inquire_point_btn = wait.until(EC.element_to_be_clickable((By.ID, "inquirePoint")))
        click(driver, inquire_point_btn)
        time.sleep(1)
        # 결제하기 버튼 클릭
        payment_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnpayment")))
        click(driver, payment_btn)
        time.sleep(1)
        # 결제 확인 팝업의 확인 버튼 클릭
        confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnConfirm01")))
        click(driver, confirm_btn)
        time.sleep(1)
        logger.info("포인트 결제 성공")
    except Exception as e:
        logging.error(f"포인트 결제 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 마이페이지 이동
def click_my_travel(driver, wait):
    try:
        my_travel_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='mypage']")))
        click(driver, my_travel_link)
        time.sleep(5)
        logger.info("마이페이지 이동 성공")
    except Exception as e:
        logging.error(f"마이페이지 이동 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 마이페이지 > 취소요청
def my_cancel_request(driver, wait, name, phoneNm):
    try:
        # 취소요청 클릭
        time.sleep(1)
        cancel_request = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/div[2]/div/div[1]/ul/li[1]/div[2]/div[2]/a')
        click(driver, cancel_request)
        time.sleep(1)
        # 접수자 입력
        driver.find_element(By.XPATH, '//*[@id="cancelerNm"]').send_keys(name)
        # 접수자 연락처 입력
        driver.find_element(By.XPATH, '//*[@id="cancelerTel"]').send_keys(phoneNm)
        # 동의접수 클릭
        time.sleep(1)
        receipt = driver.find_element(By.XPATH, '//*[@id="cancelRequestPop"]/div[2]/div[3]/button')
        click(driver, receipt)
        confirm = driver.find_element(By.XPATH, '/html/body/div[18]/div/div[6]/button[1]')
        click(driver, confirm)
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()
        # reconfirm = driver.find_element(By.XPATH, '/html/body/div[18]/div/div[6]/button[1]')
        # click(driver, reconfirm)
        logger.info("마이페이지 취소 요청 성공")
    except Exception as e:
        logging.error(f"마이페이지 취소 요청 테스트 중 오류가 발생했습니다: {str(e)}")
        return