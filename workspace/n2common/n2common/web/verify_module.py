import re, logging

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

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






