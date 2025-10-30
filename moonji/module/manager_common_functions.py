import os, logging, time, pyautogui

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from n2common.web.setup_module import click, scroll_into_view

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

# 배너명 입력
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

# 배너 url 입력
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

# 배너 이미리 업로드
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

# 관리자 팝업 클릭
def handle_popup_confirm(driver, wait, timeout=5):
    """
    [공통] HTML 팝업이 뜨면 '확인' 버튼(.btnAlert) 클릭
    --------------------------------------------------------
    - 팝업 텍스트에 따라 성공/실패 구분
    - 실패 문구 포함 시 테스트 실패 알림 후 종료
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popup"))
        )
        logger.info("✅ 팝업 감지됨")

        # 1️⃣ 팝업 텍스트 읽기
        pop_text_elem = driver.find_element(By.CSS_SELECTOR, "div.popup .pop_tit")
        popup_text = (pop_text_elem.text or "").strip()
        logger.info(f"📄 팝업 텍스트: {popup_text}")

        # 2️⃣ [확인] 버튼 클릭
        ok_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.popup .btnAlert"))
        )
        scroll_into_view(driver, ok_button)
        click(driver, ok_button)
        logger.info("✅ 팝업 [확인] 버튼 클릭 완료")

        # 3️⃣ 문구별 성공/실패 처리
        fail_keywords = ["이미", "중복", "오류", "실패", "존재", "사용중"]

        if any(word in popup_text for word in fail_keywords):
            logger.error(f"❌ 실패 팝업 감지됨: {popup_text}")
            pyautogui.alert(
                title="❌ 테스트 실패",
                text=f"테스트 실패: {popup_text}",
            )
            raise SystemExit(f"테스트 실패: {popup_text}")

        logger.info("🟢 정상 팝업 처리 완료")
        return True

    except TimeoutException:
        logger.warning("⚠️ 팝업이 표시되지 않음")
        return False

    except Exception as e:
        logger.exception(f"❌ 팝업 처리 중 오류 발생: {e}")
        raise










