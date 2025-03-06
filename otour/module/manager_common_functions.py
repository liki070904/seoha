import time, logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

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
# iframe
def iframe(driver, wait):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)

# 관리자 URL
manager_url = "https://devfss.hanatourbiz.com/login"
def manager_open(driver, wait):
    try:
        # 메인 페이지 접속
        driver.get(manager_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("매니저 페이지 열기 성공")
    except Exception as e:
        logging.error(f"매니저 페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")
# 관리자 로그인
def manager_login(driver, wait, manager_id, manager_pw, option):
    try:
        # 채널 선택 드롭다운 클릭
        channel_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nice-select.sel_md")))
        click(driver, channel_select)
        time.sleep(0.5)
        # 공급사 선택
        option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"li.option[data-value='{option}']")))
        click(driver, option)
        time.sleep(0.5)
        # ID 입력
        driver.find_element(By.ID, "userId").send_keys(manager_id)
        time.sleep(0.5)
        # 비밀번호 입력
        driver.find_element(By.ID, "userPw").send_keys(manager_pw)
        time.sleep(0.5)
        # 로그인 버튼 클릭
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogin")))
        click(driver, login_button)
        # 로그인 후 대기
        time.sleep(1)
        logger.info("관리자 페이지 로그인 성공")
    except Exception as e:
        logging.error(f"관리자 페이지 로그인 테스트 중 오류가 발생했습니다: {str(e)}")

# 예약 조회 페이지 진입
def channel_reserve_management(driver, wait):
    try:
        # 1. '예약관리' 메뉴 클릭
        reserve_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_book")))
        click(driver, reserve_menu)
        time.sleep(0.5)
        # 2. '채널예약관리' 서브메뉴 클릭
        channel_reserve = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '채널예약관리')]")))
        click(driver, channel_reserve)
        time.sleep(0.5)
        # 3. '통합예약조회' 메뉴 클릭
        integrated_reserve = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#menu_16 a")))
        click(driver, integrated_reserve)
        time.sleep(0.5)
        logger.info("예약조회 메뉴 클릭 성공")
    except Exception as e:
        logging.error(f"예약조회 메뉴 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 채널 선택 (오투어 : channelSeqArr1 / 복지몰 : channelSeqArr2 / 삼성전기 : channelSeqArr10)
def click_channel_option(driver, wait, welfare_mall_label):
    try:
        iframe(driver, wait)
        # 채널 선택 드롭다운 클릭
        channel_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='channelSeqnoBox']")))
        click(driver, channel_select)
        time.sleep(0.5)
        # 복지몰 선택
        # welfare_mall_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='{welfare_mall_label}']")))
        welfare_mall_label = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{welfare_mall_label}"]')))
        click(driver, welfare_mall_label)
        time.sleep(0.5)
        # [x] 선택
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_close")))
        click(driver, close_button)
        time.sleep(0.5)
        logger.info(f"채널 선택 성공")
    except Exception as e:
        logging.error(f"채널 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약 상세 진입
def click_search_reserve_detail(driver, wait):
    try:
        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_search")))
        click(driver, search_button)
        time.sleep(0.5)
        # 예약 상세 진입
        reserve_detail = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "table.tbl_list tbody tr td a")))
        click(driver, reserve_detail)
        time.sleep(2)
        #iframe 탈출
        driver.switch_to.default_content()
        time.sleep(2)
        logger.info("예약 상세 진입 성공")
    except Exception as e:
        logging.error(f"예약 상세 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 예약 확정
def check_reservation_status(driver, wait):
    try:
        iframe(driver,wait)
        wait_reservation_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'current') and text()='대기예약']")))
        click(driver, wait_reservation_element)
        # '예약확정' 옵션 클릭
        reservation_confirm_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.option[data-value='10']")))
        click(driver, reservation_confirm_option)
        time.sleep(0.5)
        #변경 버튼 선택
        change_button = wait.until(EC.element_to_be_clickable((By.ID, "saveResStatus")))
        click(driver, change_button)
        time.sleep(0.5)
        logger.info("예약확정 선택 성공")
    except Exception as e:
        logging.error(f"예약확정 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 결제정보 진입
def payment_info(driver, wait):
    iframe(driver,wait)
    payment_tab = driver.find_element(By.XPATH, '//*[@id="payinfo"]/a')
    click(driver,payment_tab)
















