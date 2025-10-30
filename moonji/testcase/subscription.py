import logging, pyautogui, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from n2common.web.setup_module import (setup_driver, fill_form_field, wait_for_user_input)
from n2common.web.verify_module import (get_order_number, compare_order_numbers, verify_pdf_access)
from module.homepage_common_functions import (
    intro_skip, navigation_moonji, select_gift_books, handle_delivery_address)

logger = logging.getLogger()

def main():
    driver, wait = setup_driver()
    try:
        # 🚩 1️⃣ 배송지 등록 정보 (수동 입력값)
        addr_info = {
            "delvplcNcm": "집",
            "rcvPsNm": "이서하",
            "ctpn": "01012345678",
            "search_keyword": "아차산로",
            "detail_addr": "10층 QA랩",
            "main_check": True
        }

        # 🚩 2️⃣ 문지 홈페이지 로그인
        driver.get("https://dev-moonji.ntoday.kr")
        intro_skip(driver, wait)

        fill_form_field(driver, wait, "//a[contains(text(), '로그인')]", None, field_type="click", ui_name="GNB-로그인 버튼")
        fill_form_field(driver, wait, "userId", "seoha34", field_type="text", ui_name="ID 입력")
        fill_form_field(driver, wait, "userPw", "admin135!", field_type="text", ui_name="PW 입력")
        fill_form_field(driver, wait, "//button[contains(@class, 'fill_black')]", None, field_type="click", ui_name="로그인 버튼")

        # 🚩 3️⃣ 정기구독 페이지 진입
        navigation_moonji(driver, wait, "문학과사회", "문학과사회 구독")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        fill_form_field(driver, wait, "//button[contains(., '정기구독 신청하기')]", None, field_type="click", ui_name="정기구독 신청하기")
        time.sleep(0.5)

        # 🚩 4️⃣ 구독 옵션 선택
        fill_form_field(driver, wait, "//input[@name='subscribeTerm']", "2", field_type="radio", ui_name="정기구독-구독기간")
        fill_form_field(driver, wait, ".nice-select", "151호", field_type="select", ui_name="정기구독-시작호수")

        # 🚩 5️⃣ 증정도서 선택 팝업
        fill_form_field(driver, wait, "#btnSelGiftBook", None, field_type="click", ui_name="증정도서 선택")
        # 증정도서 선택 팝업 내 도서 선택
        """
        mode=auto : 구독기간에 따른 금액까지 도서 자동 선택, subscribe_term_value=1/2/3 구독기간 년수와 동일하게 값 설정!!
        select_gift_books(driver, wait, mode="auto", subscribe_term_value="2") 
        mode=keyword : 도서 키워드 검색 선택 keyword="문학" / 검색할 키워드 입력
        select_gift_books(driver, wait, mode="keyword", keyword="문학")
        """
        select_gift_books(driver, wait, mode="auto", subscribe_term_value="2")

        # 🚩 6️⃣ 배송지 처리 (등록 여부 자동판단)
        handle_delivery_address(driver, wait, addr_info)

        # 🚩 7️⃣ 결제 약관 동의 + 결제 버튼
        fill_form_field(driver, wait, "chkAgree", None, field_type="checkbox", ui_name="결제 약관 동의")
        fill_form_field(driver, wait, "//button[contains(., '결제하기')]", None, field_type="click", ui_name="정기구독 결제하기")

        # 🚩 8️⃣ 토스 결제 수동입력 대기
        logger.info("💳 토스 결제창 오픈 — 사용자 수동 입력 모드 진입")
        wait_for_user_input("토스 결제를 직접 완료한 뒤 '확인' 버튼을 눌러주세요.")

        # 🚩 9️⃣ 결제 완료
        logger.info("✅ 사용자가 결제 완료 확인 — 자동화 재개 중...")
        logger.info("✅ 정기구독 신청 완료")

        # 정기구독 완료 페이지 - 주문번호 확인
        order_complete_num = get_order_number(driver, wait, "#orderCode", ui_name="결제 완료 페이지")

        # 🚩 🔟 마이페이지 - 정기구독 내역 진입
        fill_form_field(driver, wait, "//a[contains(text(), '마이페이지')]", None, field_type="click", ui_name="마이페이지")
        fill_form_field(driver, wait, "//a[@href='/mypage/myOrder/subscription/list']", None, field_type="click", ui_name="정기구독 내역")

        # 정기구독 내역 - 주문번호 확인
        order_list_num = get_order_number(driver, wait, ".order_list .order_num", ui_name="정기구독 내역")
        compare_order_numbers(order_complete_num, order_list_num, context="moonji_subscription")

        # PDF 서비스 신청 페이지 진입
        navigation_moonji(driver, wait, "문학과사회", "PDF 서비스 신청")
        verify_pdf_access(driver, wait)

        # ✅ 테스트 완료 알림
        pyautogui.confirm(
            title='✅ Complete',
            text='문지 정기구독 자동화 테스트 완료'
        )

    except Exception as e:
        logger.exception(f"테스트 중 오류 발생 : {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

