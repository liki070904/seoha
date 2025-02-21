import time, logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def some_function():
    logging.info("some_function 호출됨")
# 요소가 보이는 영역 안에 있도록 스크롤하는 함수
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# 스크롤 최하단으로
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 클릭
def click(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, 5, 5)  # 버튼의 (5, 5) 위치로 이동
    actions.click().perform()
# 팝업 닫기 함수
def close_popup(driver, wait, popup_id, close_button_locator):
    try:
        popup_exists = driver.execute_script(f"return document.getElementById('{popup_id}') !== null;")
        if popup_exists:
            close_button = wait.until(EC.presence_of_element_located(close_button_locator))
            scroll_into_view(driver, close_button)
            click(driver, close_button)
            print("팝업 닫기 완료")
        else:
            print("팝업이 존재하지 않습니다.")
    except Exception as e:
        print(f"팝업 닫기 중 오류 발생: {e}")
    time.sleep(2)
# 문학동네 홈페이지 진입
def home_page(driver, wait, homepage_url):
    driver.get(homepage_url)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    close_popup(driver, wait, 'popMainLayer1', (By.XPATH, '//*[@id="popMainLayer1"]/div/div[2]/button[1]'))
    time.sleep(1)
# 문학동네 로그인
def munhak_login(driver, wait, user_id, user_pw):
    login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_login[href='/login?joinChannelType=HOMEPAGE']")))
    click(driver, login_link)
    time.sleep(1)
    driver.find_element(By.ID, "userId").send_keys(user_id)
    driver.find_element(By.ID, "userPw").send_keys(user_pw)
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.fill_black")))
    click(driver, login_button)
    time.sleep(1)
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
    time.sleep(5)

    check_required_consents = driver.find_elements(By.XPATH, '//*[@id="deleteAccount"]/form/fieldset/div/div/div[3]/ul/li')
    time.sleep(1)
    check_box = driver.find_element(By.TAG_NAME, 'input')
    for check_box in check_required_consents:
        if not check_box.is_selected():
            time.sleep(0.5)
            click(driver, check_box)
    click(driver,required_consent_check)