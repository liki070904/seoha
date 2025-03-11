import time, logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from munhak.module.setup_common_functions import (click, scroll_into_view, close_popup)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# 홈페이지 url, 계정
homepage_url = "https://dev-munhak-home.ntoday.kr/"
# 문학동네 홈페이지 진입
def home_page(driver, wait):
    try:
        driver.get(homepage_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        close_popup(driver, wait, 'popMainLayer1', (By.XPATH, '//*[@id="popMainLayer1"]/div/div[2]/button[1]'))
        time.sleep(2)
        logger.info("문학동네 홈페이지 진입 성공")
    except Exception as e:
        logging.error(f"문학동네 홈페이지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 문학동네 로그인
def munhak_login(driver, wait, user_id, user_pw):
    try:
        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_login[href='/login?joinChannelType=HOMEPAGE']")))
        click(driver, login_link)
        time.sleep(1)
        driver.find_element(By.ID, "userId").send_keys(user_id)
        driver.find_element(By.ID, "userPw").send_keys(user_pw)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.fill_black")))
        click(driver, login_button)
        time.sleep(1)
        logger.info("문학동네 로그인 성공")
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 문학동네 > 마이페이지 진입
def munhak_mypage(driver):
    mypage = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/ul[2]/li[2]/a')
    click(driver, mypage)
# 문학동네 > 회원정보 변경 진입
def mydata_change(driver, userChkPwd):
    mydata_change = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div[1]/ul/li[1]/ul/li[1]')
    click(driver, mydata_change)
    driver.find_element(By.ID, "userChkPwd").send_keys(userChkPwd)
    confirm = driver.find_element(By.XPATH, '//*[@id="root"]/div[5]/div/div[2]/div[3]/button[2]')
    click(driver,confirm)
    return userChkPwd
# 문학동네 > 탈퇴 버튼 선택
def withdraw(driver):
    time.sleep(1)
    withdraw = driver.find_element(By.XPATH, '//*[@id="changeMyInfo"]/div/button')
    scroll_into_view(driver, withdraw)
    time.sleep(1)
    click(driver, withdraw)
    time.sleep(1)
    withdraw_reason = driver.find_element(By.XPATH, '//*[@id="deleteAccount"]/form/fieldset/div/div/div[2]/div/ul/li[1]/div/label')
    time.sleep(1)
    click(driver, withdraw_reason)
    required_consent_check = driver.find_element(By.XPATH, '//*[@id="deleteAccount"]/form/fieldset/div/div/div[4]/div/label')
    driver.execute_script("arguments[0].focus();", required_consent_check)
    time.sleep(1)
    check_required_consents = driver.find_elements(By.XPATH, '//*[@id="deleteAccount"]/form/fieldset/div/div/div[3]/ul/li')
    time.sleep(1)
    check_box = driver.find_element(By.TAG_NAME, 'input')
    for check_box in check_required_consents:
        if not check_box.is_selected():
            time.sleep(0.5)
            click(driver, check_box)
    click(driver,required_consent_check)
# 문학동네 > 회원탈퇴
def withdraw_confirm(driver):
    withdraw_confirm = driver.find_element(By.XPATH, '//*[@id="deleteAccount"]/div[2]/button[2]')
    click(driver, withdraw_confirm)
    time.sleep(2)
    confirm = driver.find_element(By.XPATH, '//*[@id="systemAlert"]/div[2]/div[2]/button[2]')
    click(driver, confirm)
    time.sleep(2)
    finished = driver.find_element(By.XPATH, '//*[@id="systemAlert"]/div[2]/div[2]/button')
    click(driver,finished)
# 계간 문학동네 진입
def quarterly_click(driver):
    try:
        book_author = driver.find_element(By.XPATH, '//*[@id="gnb"]/ul/li[2]/a')
        click(driver,book_author)
        time.sleep(1)
        quarterly = driver.find_element(By.XPATH, '//*[@id="gnb"]/ul/li[2]/ul/li[3]/div/ul/li[1]/a')
        click(driver,quarterly)
        time.sleep(1)
        # 계간 문학동네 정기구독 신청 클릭
        quarterly_subscription = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/div/button/span')
        click(driver, quarterly_subscription)
        time.sleep(1)
        logger.info("계간 문학동네 진입 성공")
    except Exception as e:
        logging.error(f"계간 문학동네 진입 테스트 중 오류가 발생했습니다: {str(e)}")
# 정기구독 기간 설정
def sub_date_set(driver, wait, year_id):
    try:
        label_xpath = f'//label[@for="{year_id}"]'
        year_set = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
        for_value = year_set.get_attribute("for")
        year_set_element = wait.until(EC.element_to_be_clickable((By.ID, for_value)))
        click(driver, year_set_element)
        time.sleep(1)
        logger.info(f"정기구독 기간 설정 완료 (ID: {year_id})")
    except Exception as e:
        logger.error(f"정기구독 기간 설정 중 오류 발생 (ID: {year_id}): {str(e)}")
# 정기구독 개시 설정
def sub_init_set(driver, season):
    try:
        initiation = driver.find_element(By.XPATH, '//*[@id="subscription"]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td/div/div[2]/a')
        click(driver, initiation)
        time.sleep(1)
        # 시즌별 텍스트 매핑
        season_map = {
            "봄": "봄호",
            "여름": "여름호",
            "가을": "가을호",
            "겨울": "겨울호"
        }
        # 입력한 시즌이 유효한지 확인
        if season not in season_map:
            raise ValueError(f"잘못된 입력: {season}. '봄', '여름', '가을', '겨울' 중 하나를 입력하세요.")

        season_list = driver.find_elements(By.CSS_SELECTOR, "ul.list li a")
        for element in season_list:
            if element.text == season_map[season]:
                click(driver, element)
                time.sleep(1)
                logger.info(f"정기구독 개시 계절 선택 성공: {season}")
                return
        raise ValueError(f"'{season}'에 해당하는 리스트 항목을 찾을 수 없습니다.")

    except Exception as e:
        logger.error(f"정기구독 개시 계절 선택 테스트 중 오류 발생: {str(e)}")
# 증정도서 선택
def giveaway_book(driver):
    try:
        choice_givwaway_book = driver.find_element(By.XPATH, '//*[@id="subscription"]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td/div[2]/div/button')
        click(driver, choice_givwaway_book)
        time.sleep(1)
        choice_book = driver.find_element(By.XPATH, '//*[@id="popSelectBook"]/div[2]/div[2]/ul/li[1]/div/div[1]/div/label')
        click(driver, choice_book)
        time.sleep(1)
        choice_complete = driver.find_element(By.XPATH, '//*[@id="popSelectBook"]/div[2]/div[3]/button')
        click(driver,choice_complete)
        time.sleep(1)
        logger.info("증정도서 선택 성공")
    except Exception as e:
        logger.error(f"증정도서 선택 테스트 중 오류가 발생했습니다: {str(e)}")
# 결제(쿠폰) 선택 & 동의
def payment_agree(driver):
    try:
        choice_point = driver.find_element(By.XPATH, '//*[@id="subscription"]/div[2]/div/div[1]/div[4]/table/tbody/tr[2]/td/div/div[1]/button')
        click(driver,choice_point)
        time.sleep(1)
        agree = driver.find_element(By.XPATH, '//*[@id="subscription"]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/label')
        click(driver, agree)
        time.sleep(1)
        logger.info("포인트 사용, 약관 동의 성공")
    except Exception as e:
        logger.error(f"포인트 사용,약관 동의 테스트 중 오류가 발생했습니다: {str(e)}")
# 결제하기 선택
def payment_click(driver):
    payment = driver.find_element(By.XPATH, '//*[@id="subscription"]/div[2]/div/div[2]/div[1]/div[3]/div[2]/div[2]/button')
    click(driver, payment)
    time.sleep(1)
# 마이페이지 > 정기구독 내역 진입
def my_sub_list(driver):
    sub_list = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div[1]/ul/li[2]/ul/li[4]/a')
    click(driver, sub_list)