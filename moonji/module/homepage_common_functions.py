from typing import Optional

from selenium.webdriver import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from n2common.web.setup_module import (click, fill_form_field, handle_alert)

import logging, time, re

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# 홈페이지 오픈
def homepage_open(driver, wait, url:str):
    try:
        driver.get(url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        logger.info("✅ 문지 홈페이지 열기 성공")
    except Exception as e:
        logging.error(f"문지 홈페이지 열기 테스트 중 오류가 발생했습니다: {str(e)}")

# 인트로 건너뛰기
def intro_skip(driver, wait):
    try:
        skip = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_skip')))
        click(driver, skip)
        logger.info('인트로 스킵')
    except Exception as e:
        logger.error(f'✅ 인트로 스킵 실패{e}')
        raise

# GNB 클릭
def navigation_moonji(driver, wait, main_menu: str, sub_menu: str = None):
    """
    문학과지성사 홈페이지 GNB 네비게이션 이동 함수
    ------------------------------------------------------------------
    main_menu : GNB 1차 메뉴명 (예: '문학과사회', '도서/저자')
    sub_menu  : 2차 메뉴명 (예: '문학과사회 구독', 'PDF 서비스 신청')
    ------------------------------------------------------------------
    예시:
        navigation_moonji(driver, wait, "문학과사회", "문학과사회 구독")
    """
    try:
        # 1️⃣ GNB 메인 메뉴 찾기
        main_xpath = f"//ul[@class='nav']//a[normalize-space(text())='{main_menu}']"
        main_el = wait.until(EC.element_to_be_clickable((By.XPATH, main_xpath)))
        ActionChains(driver).move_to_element(main_el).perform()
        time.sleep(0.5)
        logger.info(f"🎯 GNB 1단 메뉴 Hover 완료 → {main_menu}")

        # 2️⃣ 서브 메뉴 클릭 (필요 시)
        if sub_menu:
            sub_xpath = f"//ul[@class='nav']//ul[contains(@class,'depth')]//a[normalize-space(text())='{sub_menu}']"
            sub_el = wait.until(EC.element_to_be_clickable((By.XPATH, sub_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sub_el)
            time.sleep(0.3)
            sub_el.click()
            logger.info(f"✅ GNB 2단 메뉴 클릭 완료 → {sub_menu}")
            time.sleep(0.5)
        else:
            # 2차 메뉴가 없으면 1차 메뉴 클릭
            main_el.click()
            logger.info(f"✅ GNB 1단 메뉴 클릭 완료 → {main_menu}")

        # 3️⃣ 페이지 이동 대기
        time.sleep(1.5)
        logger.info(f"🎯 GNB 이동 성공: {main_menu} > {sub_menu if sub_menu else '-'}")

    except Exception as e:
        logger.error(f"❌ GNB 이동 실패 ({main_menu} > {sub_menu}): {e}")
        raise

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

# 정기구독-증정도서 선택
# ======================================================================
# 🎯 1️⃣ 자동 선택형 — 구독기간(1/2/3)에 따른 금액 한도 내에서 자동 선택
# ======================================================================
def select_gift_books_auto(driver, wait, subscribe_term_value: str):
    """증정도서 자동선택 (JS 기반 초고속 + 안정형 대기 포함)"""
    try:
        # 1️⃣ 팝업 활성화 대기
        popup = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#popGiftBook.pop_layer.active"))
        )
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".book_select li")))
        time.sleep(0.3)  # 첫 렌더링 안정화용 딜레이 (0.3초 이하 권장)

        limit_map = {"1": 30000, "2": 60000, "3": 90000}
        limit = limit_map.get(str(subscribe_term_value), 0)
        logger.info(f"⚡ 증정 도서 자동선택 시작 (한도: {limit:,}원)")

        # 2️⃣ JS 한 번으로 모든 도서 정보 수집
        script = """
        const books = [...document.querySelectorAll('.book_select li')];
        return books.map(li => {
            const title = li.querySelector('.tit')?.innerText?.trim() || '';
            const price = li.querySelector('.price')?.innerText?.trim() || '';
            const id = li.querySelector('input[type=checkbox]')?.id || '';
            return { title, price, id };
        }).filter(b => b.title && b.price && b.id);
        """
        books = driver.execute_script(script)

        if not books:
            logger.warning("⚠ 선택 가능한 도서가 없습니다 (book_select 비어있음).")
            return

        selected_sum = 0
        selected_titles = []

        # 3️⃣ 브라우저 내부에서 직접 클릭
        for b in books:
            try:
                price = int(re.sub(r"[^0-9]", "", b["price"]))
                if selected_sum + price > limit:
                    continue

                driver.execute_script(f"document.getElementById('{b['id']}').click();")
                selected_sum += price
                selected_titles.append(f"{b['title']} ({price:,}원)")
                logger.info(f"🟩 도서 선택됨: {b['title']} ({price:,}원)")
                time.sleep(0.5)

                if limit - selected_sum < 1000:
                    break
            except Exception:
                continue

        # 4️⃣ 결과 로그
        if selected_titles:
            logger.info(f"✅ 선택 완료: {', '.join(selected_titles)} (총 {selected_sum:,}원 / 한도 {limit:,}원)")
        else:
            logger.warning("⚠ 선택된 도서 없음")

        # 5️⃣ 선택완료 버튼 클릭 (JS 방식)
        driver.execute_script("""
            const btn = document.querySelector('#btnSelect');
            if (btn) { btn.click(); }
        """)
        logger.info("✅ '선택완료' 버튼 클릭 완료 (팝업 닫힘)")

    except TimeoutException:
        logger.error("❌ 증정 도서 팝업 로딩 실패 (#popGiftBook.pop_layer.active)")
        raise
    except Exception as e:
        logger.error(f"❌ 도서 선택 중 오류 → {e}")
        raise

# ======================================================================
# 🎯 2️⃣ 키워드 기반 선택형 — 제목에 특정 단어가 포함된 도서만 선택
# ======================================================================
def select_gift_books_by_keyword(driver, wait, keyword: str):
    """팝업 내 검색 기능을 활용한 키워드 기반 도서 선택"""
    try:
        popup = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#popGiftBook.pop_layer.active"))
        )
        time.sleep(0.5)

        keyword = keyword.strip()
        logger.info(f"🎯 [키워드모드] 증정 도서 선택 시작 (검색어: '{keyword}')")

        # 🔹 1️⃣ 검색어 입력
        search_input = popup.find_element(By.CSS_SELECTOR, "#searchWord")
        search_input.clear()
        search_input.send_keys(keyword)
        logger.info(f"✅ 검색어 입력 완료 → {keyword}")

        # 🔹 2️⃣ 검색 버튼 클릭
        search_btn = popup.find_element(By.CSS_SELECTOR, ".btn_search")
        click(driver, search_btn)
        logger.info("✅ 검색 버튼 클릭")

        # 🔹 3️⃣ 검색 결과 대기 (book_select 갱신)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".book_select li")))
        time.sleep(1.0)

        books = popup.find_elements(By.CSS_SELECTOR, ".book_select li")
        if not books:
            logger.warning(f"⚠ '{keyword}' 검색 결과가 없습니다.")
            return

        selected_titles = []
        for book in books:
            try:
                title = book.find_element(By.CSS_SELECTOR, ".tit").text.strip()
                label = book.find_element(By.CSS_SELECTOR, "label")
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
                click(driver, label)
                selected_titles.append(title)
                time.sleep(0.2)
            except Exception as e:
                logger.warning(f"⚠ 도서 선택 중 오류 → {e}")

        logger.info(f"✅ 검색 결과 선택 완료: {', '.join(selected_titles)}")

        # 🔹 4️⃣ 선택완료 버튼 클릭
        select_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSelect")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_btn)
        click(driver, select_btn)
        logger.info("✅ '선택완료' 버튼 클릭 완료 (팝업 닫힘)")

    except TimeoutException:
        logger.error("❌ 증정 도서 팝업을 찾을 수 없습니다 (#popGiftBook.pop_layer.active)")
        raise
    except Exception as e:
        logger.error(f"❌ 키워드 기반 도서 선택 중 오류 → {e}")
        raise

# ======================================================================
# 🎯 3️⃣ 통합 진입 함수 — 모드 선택 (auto / keyword)
# ======================================================================
def select_gift_books(driver, wait, mode="auto", **kwargs):
    """
    증정 도서 선택 통합 함수
    mode: "auto" 또는 "keyword"
    kwargs:
        - subscribe_term_value="2"  (auto 모드용)
        - keyword="문학"             (keyword 모드용)
    """
    if mode == "auto":
        select_gift_books_auto(driver, wait, kwargs.get("subscribe_term_value"))
    elif mode == "keyword":
        select_gift_books_by_keyword(driver, wait, kwargs.get("keyword"))
    else:
        raise ValueError("❌ select_gift_books() mode는 'auto' 또는 'keyword'만 허용됩니다.")

# 배송정보 입력 - 배송지 없으면 등록 클릭 있으면 패스
def handle_delivery_address(driver, wait, addr_info: dict):
    """
    📦 배송지 확인 및 자동 등록
    ------------------------------------------------------
    - 배송지 없을 시: 실행파일에서 전달받은 addr_info로 자동 등록
    - 배송지 있을 시: 아무 동작 안 함
    ------------------------------------------------------
    addr_info keys:
        delvplcNcm, rcvPsNm, ctpn, search_keyword, detail_addr, main_check
    """
    try:
        delivery_area = wait.until(EC.presence_of_element_located((By.ID, "deliveryArea")))
        address_texts = delivery_area.find_elements(By.CSS_SELECTOR, ".txt_address.no")

        if address_texts and "배송지를 추가하세요" in address_texts[0].text.strip():
            logger.info("📦 배송지 없음 → 신규 배송지 등록 시작")

            add_btn = delivery_area.find_element(By.CSS_SELECTOR, "button[onclick*='fn_popDelivery']")
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
            click(driver, add_btn)
            logger.info("✅ '배송지 추가' 버튼 클릭 완료")

            open_delivery_popup(driver, wait)
            time.sleep(1)

            fill_delivery_form(
                driver, wait,
                delvplcNcm=addr_info.get("delvplcNcm", "집"),
                rcvPsNm=addr_info.get("rcvPsNm", "이서하"),
                ctpn=addr_info.get("ctpn", "01000000000"),
                search_keyword=addr_info.get("search_keyword", "서울특별시"),
                detail_addr=addr_info.get("detail_addr", ""),
                main_check=addr_info.get("main_check", True)
            )

            submit_delivery(driver, wait)
            handle_alert(driver)
            logger.info("✅ 신규 배송지 등록 완료")
        else:
            logger.info("📦 기존 배송지 존재 → 등록 생략")

    except Exception as e:
        logger.error(f"❌ 배송지 처리 중 오류 발생: {e}")
        raise

# ======================================================================
# 1️⃣ 배송지 등록 팝업 오픈
# ======================================================================
def open_delivery_popup(driver, wait):
    """
    📦 배송지 변경 팝업 내부의 [+배송지 등록] 버튼 클릭
    (dim 내부 포함 → popup 범위 한정 class 기반 탐색)
    """
    try:
        # 팝업 활성화 대기
        popup = wait.until(EC.visibility_of_element_located((By.ID, "popDelivery")))
        assert popup.is_displayed(), "배송지 변경 팝업이 표시되지 않음"
        logger.info("✅ 배송지 변경 팝업 열림 확인")

        # 팝업 내부 버튼을 클래스명으로 찾기
        add_btn = popup.find_element(By.CSS_SELECTOR, "button.btn_xs.pc_btn_sm.line_grey60")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
        time.sleep(0.2)

        # 내부 dim 존재할 수 있으므로 JS 클릭 보정 포함
        try:
            click(driver, add_btn)
        except Exception:
            logger.warning("⚠ dim이 클릭을 방해 — JS로 강제 클릭")
            driver.execute_script("arguments[0].click();", add_btn)

        logger.info("📦 [+배송지 등록] 버튼 클릭 완료 (팝업 내부 클래스 기반)")

        # 등록 팝업 뜰 때까지 대기
        wait.until(EC.visibility_of_element_located((By.ID, "popDeliveryRegister")))
        logger.info("✅ 배송지 등록 팝업 표시 확인 완료")

    except Exception as e:
        logger.error(f"❌ 배송지 변경 팝업 내부 버튼 클릭 실패: {e}")
        raise

# ======================================================================
# 2️⃣ 주소검색
# ======================================================================
def search_addr(driver, keyword: Optional[str] = None):
    """주소검색 버튼 클릭 → 새창에서 검색어 입력 → 첫 번째 주소 선택 → 복귀"""
    try:
        search_btn = driver.find_element(By.XPATH, "//button[span[text()='검색하기']]")
        click(driver, search_btn)
        logger.info("📍 [검색하기] 버튼 클릭 완료")

        # 새창 전환
        original_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in driver.window_handles if w != original_window][0]
        driver.switch_to.window(new_window)
        logger.info("🪟 주소검색 새창으로 전환 완료")

        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

        search_box = driver.find_element(By.CSS_SELECTOR, "input")
        search_box.clear()
        search_box.send_keys(keyword or "")
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        logger.info(f"🔍 주소검색어 입력 및 실행: {keyword or '기본검색'}")

        # 첫 번째 주소 선택
        first_addr = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.link_post span.txt_addr"))
        )
        click(driver, first_addr)
        logger.info("✅ 첫 번째 주소 클릭 완료")

        # 창 닫힘 → 원래 화면 복귀
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
        driver.switch_to.window(original_window)
        logger.info("↩ 원래 메인 창으로 복귀 완료")

    except Exception as e:
        logger.error(f"❌ 주소검색 실패: {e}")
        raise

# ======================================================================
# 3️⃣ 배송지 등록 입력 (정상 순서)
# ======================================================================
def fill_delivery_form(driver, wait,
                       delvplcNcm: str,
                       rcvPsNm: str,
                       ctpn: str,
                       search_keyword: Optional[str] = None,
                       detail_addr: str = "",
                       main_check: bool = False
                       ):
    """
    📝 배송지 등록 팝업에서 정보 입력 및 주소검색 처리
    순서:
      1) 배송지명 / 받는분 / 연락처 입력
      2) 주소검색 (새창)
      3) 상세주소 입력
      4) 기본배송지 체크
    """
    try:
        popup = wait.until(EC.visibility_of_element_located((By.ID, "popDeliveryRegister")))
        assert "active" in popup.get_attribute("class"), "배송지 등록 팝업이 활성화되지 않음"
        logger.info("✅ 배송지 등록 팝업 표시 확인")

        # 1️⃣ 기본정보 입력
        fill_form_field(driver, wait, "delvplcNcm", delvplcNcm)
        fill_form_field(driver, wait, "rcvPsNm", rcvPsNm)
        fill_form_field(driver, wait, "ctpn", ctpn)
        logger.info("📝 배송지명 / 받는분 / 연락처 입력 완료")

        # 2️⃣ 주소검색
        search_addr(driver, keyword=search_keyword)
        logger.info("📍 주소검색 및 자동입력 완료")

        # 3️⃣ 상세주소 입력
        fill_form_field(driver, wait, "dtlAdres", detail_addr)
        logger.info(f"🏠 상세주소 입력 완료: {detail_addr}")

        # 4️⃣ 기본배송지 체크
        if main_check:
            chk = driver.find_element(By.ID, "mainAt")
            if not chk.is_selected():
                click(driver, chk)
                logger.info("🏠 기본 배송지로 설정 체크 완료")

    except TimeoutException:
        logger.error("❌ 배송지 등록 팝업 또는 주소검색 로딩 실패 (#popDeliveryRegister)")
        raise
    except Exception as e:
        logger.error(f"❌ 배송지 입력 중 오류 발생: {e}")
        raise

# ======================================================================
# 4️⃣ 등록 버튼 클릭 및 팝업 닫힘 대기
# ======================================================================
def submit_delivery(driver, wait):
    """🚀 [등록] 버튼 활성화 대기 후 클릭 → 팝업 닫힘 확인"""
    try:
        save_btn = wait.until(EC.presence_of_element_located((By.ID, "saveBtn")))
        wait.until(lambda d: save_btn.is_enabled())
        click(driver, save_btn)
        logger.info("✅ [등록] 버튼 클릭 완료")

        wait.until(EC.invisibility_of_element_located((By.ID, "popDeliveryRegister")))
        logger.info("📦 배송지 등록 팝업 닫힘 확인")
    except Exception as e:
        logger.error(f"❌ 배송지 등록 제출 중 오류 발생: {e}")
        raise

# todo
# setup_module에 있는 함수로 사용 > 이슈 없으면 삭제 예정
# # 브라우저 알럿 닫기
# def handle_alert(driver, timeout=5):
#     try:
#         WebDriverWait(driver, timeout).until(EC.alert_is_present())
#         alert = Alert(driver)
#         msg = alert.text
#         logger.info(f"📢 Alert 표시됨: {msg}")
#         alert.accept()  # '확인' 클릭
#         logger.info("✅ Alert 자동 닫기 완료")
#         time.sleep(0.5)
#         return msg
#     except NoAlertPresentException:
#         logger.warning("⚠ Alert가 표시되지 않았습니다.")
#     except Exception as e:
#         logger.error(f"❌ Alert 처리 중 오류: {e}")
#         raise


