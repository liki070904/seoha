import re, logging, time

import pyautogui
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from n2common.web.setup_module import handle_alert

logger = logging.getLogger(__name__)

# 주문번호 추출
def get_order_number(driver, wait, selector: str, ui_name: str = "주문번호"):
    """
    ✅ 페이지에서 주문번호 추출 (숫자/문자 조합 지원)
    -----------------------------------------------------------------
    selector : 주문번호가 표시된 요소 선택자
                (#, ., // 모두 가능 — fill_form_field와 동일)
    ui_name  : 로깅용 이름
    -----------------------------------------------------------------
    반환값: 추출된 주문번호 문자열 (예: '2025102300000004', 'GFT12345A')
    -----------------------------------------------------------------
    """
    try:
        # selector 타입 판별
        by_type = (
            By.XPATH if selector.startswith("//")
            else By.CSS_SELECTOR if selector.startswith((".", "#"))
            else By.ID
        )

        # 1️⃣ order_list 전체 로드 대기
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.order_list")))

        # 2️⃣ 모든 주문번호 요소가 렌더될 때까지 대기
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".order_num")))

        # 3️⃣ 지정 selector로 모든 요소 가져오기
        elements = driver.find_elements(by_type, selector)
        if not elements:
            raise TimeoutException(f"{ui_name} 요소를 찾지 못했습니다 ({selector})")

        logger.info(f"📦 {ui_name}에서 {len(elements)}개의 주문번호 감지됨")

        # 4️⃣ 첫 번째 요소만 추출
        el = elements[0]
        text = el.text.strip()
        match = re.search(r"([A-Za-z0-9-]+)", text)
        if not match:
            raise ValueError(f"{ui_name}에서 주문번호를 인식하지 못함: {text}")
        order_num = match.group(1)

        logger.info(f"🧾 {ui_name} 첫 번째 주문번호 추출 완료 → {order_num}")
        return order_num

    except Exception as e:
        logger.error(f"❌ {ui_name} 주문번호 추출 실패: {e}")
        raise

# 추출한 주문번호 비교
def compare_order_numbers(order_num_1: str, order_num_2: str, context: str = "기본"):
    """
    ✅ 두 주문번호 비교 및 결과 로그
    -----------------------------------------------------------------
    order_num_1 : 첫 번째 주문번호 (예: 결제 완료 페이지)
    order_num_2 : 두 번째 주문번호 (예: 내역 페이지)
    context     : 로그 구분용 (moonji / giftian / kolmar 등)
    -----------------------------------------------------------------
    """
    try:
        if not order_num_1 or not order_num_2:
            raise ValueError("비교할 주문번호가 누락되었습니다.")

        if order_num_1 == order_num_2:
            logger.info(f"✅ [{context}] 주문번호 일치 확인 완료: {order_num_1}")
            return True
        else:
            logger.warning(
                f"⚠ [{context}] 주문번호 불일치 → 결제:{order_num_1} / 내역:{order_num_2}"
            )
            return False

    except Exception as e:
        logger.error(f"❌ [{context}] 주문번호 비교 중 오류 발생: {e}")
        raise

# 윈도우 새창(탭) 감지 후 전환
def switch_to_new_window(driver, delay: float = 2.0, timeout: int = 10):
    """
    ✅ 새창(탭) 감지 후 전환
    - delay: 창이 열릴 여유 시간
    - timeout: 창 개수 감지 최대 대기시간
    """
    logger.info(f"🕓 새창 생성 대기 중 (delay={delay}s)...")
    time.sleep(delay)  # 새창 뜨는 여유시간 확보

    WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > 1)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    logger.info("🪟 새창 전환 완료")
    return driver.current_window_handle

# URL 검증
def verify_url(
        driver,
        expected: str,
        *,
        exact: bool = False,
        switch_new_window: bool = False,
        timeout: int = 10,
        delay: float = 2.0  # ✅ 새창 로딩 여유 시간
):
    """
    URL 검증 통합 함수 (간소화 + 안정형)
    --------------------------------
    - 새창이 느리게 열릴 때를 대비해 sleep(delay) 적용
    - 전체 일치(exact=True) 또는 포함 여부 비교(default)
    """
    try:
        current_url = WebDriverWait(driver, timeout).until(lambda d: d.current_url)
        logger.info(f"현재 URL: {current_url}")

        # URL 비교
        if exact:
            if current_url == expected:
                logger.info(f"✅ URL 정확 일치: {current_url}")
                return True
            else:
                logger.error(f"❌ URL 불일치 (기대: {expected}, 실제: {current_url})")
                raise AssertionError(f"URL 불일치: 기대='{expected}', 실제='{current_url}'")
        else:
            if expected in current_url:
                logger.info(f"✅ URL 포함 검증 성공: '{expected}' in '{current_url}'")
                return True
            else:
                logger.error(f"❌ URL 불일치 (기대 포함: '{expected}', 실제: '{current_url}')")
                raise AssertionError(f"URL 불일치: '{current_url}' (기대 포함: '{expected}')")

    except Exception as e:
        logger.exception(f"URL 검증 중 오류 발생: {e}")
        raise

# pdf 서비스 신청 페이지 알럿 노출 검증
def verify_pdf_access(driver, wait, *, expected_alert_text="정기구독 신청자 전용 서비스입니다."):
    """
    ✅ PDF 서비스 접근 검증 모듈
    - 정기구독중인 계정은 알럿이 없어야 정상
    - 알럿이 뜨면 정기구독 미반영 or 권한 오류로 판단

    Args:
        driver: WebDriver 인스턴스
        wait: WebDriverWait 인스턴스
        expected_alert_text (str): 접근 제한 알럿 문구 (기본값: '정기구독 신청자 전용 서비스입니다.')

    Returns:
        bool: True = 접근 성공 (정기구독 중), False = 접근 제한 (정기구독 미반영)
    """
    try:
        # 🚩 알럿 검증
        alert_text = handle_alert(driver, expected_text=expected_alert_text)

        if alert_text:
            logger.warning(f"⚠️ 접근 제한 알럿 발생: {alert_text}")
            pyautogui.alert("⚠️ 정기구독 미반영 — PDF 서비스 접근 제한 알럿 발생", "검증 실패")
            return False

        logger.info("✅ 알럿 없음 — PDF 서비스 페이지 정상 접근 (정기구독중 계정)")
        return True

    except Exception as e:
        logger.exception(f"❌ PDF 접근 검증 중 오류 발생: {e}")
        return False


