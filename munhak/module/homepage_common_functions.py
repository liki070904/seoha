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
def munhak_mypage(driver, wait):
    mypage = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/ul[2]/li[2]/a')
    click(driver, mypage)
# 문학동네 > 회원정보 변경 진입
def mydata_change(driver, wait, userChkPwd):
    mydata_change = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div[1]/ul/li[1]/ul/li[1]')
    click(driver, mydata_change)
    driver.find_element(By.ID, "userChkPwd").send_keys(userChkPwd)
    confirm = driver.find_element(By.XPATH, '//*[@id="root"]/div[5]/div/div[2]/div[3]/button[2]')
    click(driver,confirm)
    return userChkPwd
# 문학동네 > 탈퇴 버튼 선택
def withdraw(driver, wait):
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
def withdraw_confirm(driver, wait):
    withdraw_confirm = driver.find_element(By.XPATH, '//*[@id="deleteAccount"]/div[2]/button[2]')
    click(driver, withdraw_confirm)
    time.sleep(2)
    confirm = driver.find_element(By.XPATH, '//*[@id="systemAlert"]/div[2]/div[2]/button[2]')
    click(driver, confirm)
    time.sleep(2)
    finished = driver.find_element(By.XPATH, '//*[@id="systemAlert"]/div[2]/div[2]/button')
    click(driver,finished)