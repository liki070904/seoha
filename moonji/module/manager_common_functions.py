import os, logging, time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from n2common.web.setup_module import click, iframe, scroll_into_view

logger = logging.getLogger(__name__)

# ========================================
# 1️⃣ 관리자 기본 접근 / 네비게이션
# ========================================

def manager_open(driver, wait, url: str):
    """관리자 페이지 접속"""
    try:
        driver.get(url)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        logger.info("✅ 관리자 페이지 접속 성공")
    except Exception as e:
        logger.error(f"❌ 관리자 페이지 열기 실패: {e}")
        raise


def manager_login(driver, wait, manager_id: str, manager_pw: str):
    """관리자 로그인"""
    try:
        driver.find_element(By.ID, "userId").send_keys(manager_id)
        driver.find_element(By.ID, "userPw").send_keys(manager_pw)
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogin")))
        click(driver, login_button)
        logger.info(f"✅ 관리자 로그인 성공: {manager_id}")
    except Exception as e:
        logger.error(f"❌ 관리자 로그인 실패: {e}")
        raise


# ========================================
# 2️⃣ 배너 관리 공통 영역
# ========================================

def select_nice_option(driver, wait, select_id: str, option_text: str):
    """nice-select 공통 선택"""
    try:
        wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"#{select_id} + .nice-select")))
        span = wrapper.find_element(By.CSS_SELECTOR, "span.current")
        click(driver, span)

        options = wrapper.find_elements(By.CSS_SELECTOR, "ul.list li.option")
        for opt in options:
            if opt.text.strip() == option_text.strip():
                click(driver, opt)
                logger.info(f"✅ '{select_id}' 옵션 선택 완료 → {option_text}")
                return
        raise ValueError(f"'{option_text}' 옵션을 '{select_id}'에서 찾지 못했습니다")
    except Exception as e:
        logger.exception(f"❌ select_nice_option 오류: {e}")
        raise


def select_checkbox_list(driver, wait, area_selector: str, label_list: list[str], *, checked=True):
    """범용 체크박스 리스트 선택"""
    try:
        if not area_selector.startswith(('.', '#')):
            area_selector = f"#{area_selector}"

        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, area_selector)))

        for label_text in label_list:
            try:
                label_xpath = f".//label[normalize-space(text())='{label_text}']"
                label_el = container.find_element(By.XPATH, label_xpath)
                checkbox_el = label_el.find_element(By.XPATH, "./preceding-sibling::input[@type='checkbox']")
                if checked and not checkbox_el.is_selected():
                    click(driver, label_el)
                    logger.info(f"✅ '{label_text}' 체크 완료")
                elif not checked and checkbox_el.is_selected():
                    click(driver, label_el)
                    logger.info(f"✅ '{label_text}' 해제 완료")
            except Exception:
                logger.warning(f"⚠ '{label_text}' 항목을 찾지 못했습니다.")
        logger.info(f"🟢 체크박스 영역({area_selector}) 처리 완료")

    except Exception as e:
        logger.exception(f"❌ select_checkbox_list 오류: {e}")
        raise


def input_banner_name(driver, banner_name: str):
    """배너명 입력"""
    try:
        field = driver.find_element(By.ID, "bannerName")
        field.clear()
        field.send_keys(banner_name)
        logger.info(f"✅ 배너명 입력 완료: {banner_name}")
    except Exception as e:
        logger.error(f"❌ 배너명 입력 실패: {e}")
        raise


def input_banner_url(driver, device: str, url: str):
    """배너 URL 입력 (PC/모바일)"""
    try:
        field_id = f"{device}Url"
        field = driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(url)
        logger.info(f"✅ {device.upper()} URL 입력 완료: {url}")
    except Exception as e:
        logger.error(f"❌ {device.upper()} URL 입력 실패: {e}")
        raise


def upload_banner_image_common(driver, wait, device: str, file_path: str):
    """배너 이미지 업로드 (PC/모바일)"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        file_input_id = "attachedFileImg01" if device == "pc" else "attachedFileImg03"
        file_input = wait.until(EC.presence_of_element_located((By.ID, file_input_id)))
        file_input.send_keys(file_path)
        logger.info(f"✅ {device.upper()} 이미지 업로드 완료: {os.path.basename(file_path)}")
    except Exception as e:
        logger.exception(f"❌ {device.upper()} 이미지 업로드 실패: {e}")
        raise


def set_banner_period(driver, wait, start_date: str, end_date: str):
    """배너 노출 기간 설정"""
    try:
        # ✅ 시작일
        start_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "stDt"))
        )
        # driver.execute_script("arguments[0].scrollIntoView(true);", start_input)
        scroll_into_view(driver, start_input)
        start_input.clear()
        start_input.send_keys(start_date)
        logger.info(f"✅ 시작일 입력 완료: {start_date}")

        # ✅ 종료일
        end_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "edDt"))
        )
        # driver.execute_script("arguments[0].scrollIntoView(true);", end_input)
        scroll_into_view(driver, end_input)
        end_input.clear()
        end_input.send_keys(end_date)
        logger.info(f"✅ 종료일 입력 완료: {end_date}")

        time.sleep(0.5)

    except Exception as e:
        logger.error(f"❌ 배너 기간 설정 실패: {str(e)}")
        raise


def select_radio_by_label(driver, wait, area_selector: str, label_text: str):
    """라디오 버튼 선택"""
    try:
        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, area_selector)))
        label_xpath = f".//label[normalize-space(text())='{label_text}']"
        label_el = container.find_element(By.XPATH, label_xpath)
        click(driver, label_el)
        logger.info(f"✅ 라디오 '{label_text}' 선택 완료")
    except Exception as e:
        logger.exception(f"❌ 라디오 선택 실패: {e}")
        raise


# ========================================
# 3️⃣ 예약/결제 관리 전용 (복지몰)
# ========================================
# ⚠️ 예약 관련 함수는 추후 별도 파일로 분리 권장

def channel_cancel_management(driver, wait):
    """복지몰 취소요청 조회 메뉴 진입"""
    try:
        click(driver, wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico_book"))))
        click(driver, wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '채널예약관리')]"))))
        click(driver, wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu_51"]/a'))))
        logger.info("✅ 복지몰 취소요청조회 메뉴 진입 완료")
    except Exception as e:
        logger.error(f"❌ 복지몰취소요청조회 메뉴 실패: {e}")

# 취소요청건 진입
def cancel_request_info(driver, wait):
    try:
        cancel_req_info = driver.find_element(By.XPATH, '//*[@id="table_canceled"]/tbody/tr[1]/td[5]/a')
        click(driver,cancel_req_info)
        time.sleep(1)
        logger.info("취소요청 진입 성공")
    except Exception as e:
        logging.error(f"취소요청 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return

# 환불요청
def payback_request(driver, wait, cancel_reason):
    try:
        reason = driver.find_element(By.XPATH, '//*[@id="tbl_resinfo_payment_his"]/tbody/tr[3]/td[1]/div/div/span')
        click(driver, reason)
        time.sleep(1)
        all_cancel = driver.find_element(By.XPATH, '//*[@id="tbl_resinfo_payment_his"]/tbody/tr[3]/td[1]/div/div/div/ul/li[2]')
        click(driver, all_cancel)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="note"]').send_keys(cancel_reason)
        time.sleep(1)
        cancel_save = driver.find_element(By.XPATH, '//*[@id="savePayinfo"]')
        click(driver, cancel_save)
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(1)
        logger.info("환불 요청 성공")
    except Exception as e:
        logging.error(f"환불 요청 테스트 중 오류가 발생했습니다: {str(e)}")
        return

# 예약정보 탭 > 상태값 취소 변경
def status_cancel(driver, wait):
    try:
        time.sleep(2)
        reserve_tab = driver.find_element(By.XPATH, '//*[@id="resinfo"]/a')
        click(driver, reserve_tab)
        time.sleep(1)
        reserve_status = driver.find_element(By.XPATH, '//*[@id="tbl_resinfo_detail"]/tbody/tr[3]/td[1]/div/span')
        click(driver, reserve_status)
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 10);")
        cancel = driver.find_element(By.XPATH, '//*[@id="tbl_resinfo_detail"]/tbody/tr[3]/td[1]/div/div/ul/li[6]')
        click(driver, cancel)
        time.sleep(1)
        change_status = driver.find_element(By.XPATH, '//*[@id="saveResStatus"]')
        click(driver, change_status)
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(1)
        logger.info("예약정보 진입, 상태값 취소 변경 성공")
    except Exception as e:
        logging.error(f"예약정보 진입, 상태값 취소 변경 테스트 중 오류가 발생했습니다: {str(e)}")
        return

# 취소정보 저장
def save_to_cancel_info(driver, wait):
    try:
        time.sleep(1)
        cancel_status = driver.find_element(By.XPATH, '//*[@id="tbl_cancel"]/tbody/tr[2]/td[2]/div/span')
        click(driver, cancel_status)
        cancel_reason = driver.find_element(By.XPATH, '//*[@id="tbl_cancel"]/tbody/tr[2]/td[2]/div/div/ul/li[2]')
        click(driver, cancel_reason)
        save_status = driver.find_element(By.XPATH, '//*[@id="saveResinfo"]/span')
        click(driver, save_status)
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(1)
        logger.info("취소정보 저장 성공")
    except Exception as e:
        logging.error(f"취소정보 저장 테스트 중 오류가 발생했습니다: {str(e)}")
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
    try:
        payment_tab = driver.find_element(By.XPATH, '//*[@id="payinfo"]/a')
        click(driver,payment_tab)
        logger.info("결제정보 진입 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"결제정보 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return











