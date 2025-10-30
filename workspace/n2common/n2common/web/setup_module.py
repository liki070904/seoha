import pyautogui, os, time, logging, re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

import tkinter as tk

# ✅ 로깅 설정 추가 (모듈 로드 시 자동 설정)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

IFRAME_PATHS = {
    "asIsAdmin" : '//*[@id="myTabbar"]/div/div/div[3]/div/iframe',
    "asIsAdminCancel" : '//*[@id="myTabbar"]/div/div/div[4]/div/iframe',
    "toBeAdmin" : '//*[@id="ifr_menu_26"]'}

# path
def get_current_dir():
    """현재 파일이 위치한 디렉토리 반환"""
    return os.path.dirname(os.path.abspath(__file__))
def get_parent_dir(level=1):
    """현재 파일의 상위 디렉토리 반환 (기본적으로 한 단계 위)"""
    current_dir = get_current_dir()
    return os.path.abspath(os.path.join(current_dir, *[".."] * level))

# 드라이버 설정
def setup_driver():
    # Chrome WebDriver 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--force-device-scale-factor=0.9")
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.page_load_strategy = "eager"
    # WebDriver 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 대기 설정
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 3)
    return driver, wait

# 요소가 보이는 영역 안에 있도록 스크롤하는 함수
def scroll_into_view(driver, element=None, bottom=False):
    if bottom:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    else:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

# 클릭
def click(driver, element):
    """
    단순 .click() 대신 실제 마우스 이벤트 체인을 발생시키는 클릭
    (UI상에서 hover/onclick 동작 모두 트리거됨)
    """
    driver.execute_script("""
        const el = arguments[0];
        ['mouseenter', 'mouseover', 'mousedown', 'mouseup', 'click'].forEach(evtType => {
            el.dispatchEvent(new MouseEvent(evtType, {
                bubbles: true,
                cancelable: true,
                view: window
            }));
        });
    """, element)

# 팝업 닫기 함수
def close_popup(driver, wait, popup_id, close_button_locator):
    try:
        popup_exists = driver.execute_script(f"return document.getElementById('{popup_id}') !== null;")
        if popup_exists:
            close_button = wait.until(EC.presence_of_element_located(close_button_locator))
            scroll_into_view(driver, close_button)
            click(driver, close_button)
            logger.info("팝업 닫기 완료")
        else:
            logger.error("팝업이 존재하지 않습니다.")
    except Exception as e:
        print(f"팝업 닫기 중 오류 발생: {e}")

# 알럿 확인
def handle_alert(driver, expected_text=None, html=False, timeout=5):
    if html: # check_html_alert_text
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.find_element(By.XPATH, '//*[@id="alert"]/div[2]/div[1]/strong').is_displayed()
            )
            alert_elem = driver.find_element(By.XPATH, '//*[@id="alert"]/div[2]/div[1]/strong')
            alert_text = alert_elem.text.strip()
            print(f"[DEBUG] HTML Alert 텍스트: {alert_text}")

            if expected_text:
                return expected_text in alert_text
            return alert_text  # expected_text가 없으면 텍스트 자체를 리턴
        except (TimeoutException, NoSuchElementException) as e:
            logging.warning(f"[HTML Alert 탐색 실패] {e}")
            return False
    else: # accept_basic_alert
        try:
            WebDriverWait(driver, timeout).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            time.sleep(1)
            logging.info(f"얼럿 수락됨: {alert_text}")
            return alert_text
        except:
            logging.warning("알림창이 없어 스킵합니다.")
            return None

# 토스트 팝업
def show_toast(message, duration):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    bg_color = "#222222"
    toast_width = 600
    toast_height = 70

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - toast_width - 30
    y = screen_height - toast_height - 60

    root.configure(bg=bg_color)
    root.geometry(f"{toast_width}x{toast_height}+{x}+{y}")

    label = tk.Label(
        root, text=message,
        bg=bg_color, fg="white",
        font=("Arial", 14),
        padx=20, pady=15,
        bd=0, highlightthickness=0
    )
    label.pack(expand=True, fill="both")

    def close_toast():
        root.destroy()
        logging.info(f"[토스트 종료] {message}")  # ← 토스트 닫힐 때 로그 찍힘

    root.after(int(duration * 1000), close_toast)
    root.mainloop()

# 공통 iframe 전환 함수
def switch_iframe(driver, key: str):
    """
    지정된 키(asIsAdmin, asIsAdminCancel, toBeAdmin 등)에 해당하는 iframe으로 전환.
    예: switch_iframe(driver, "toBeAdmin")
    """
    try:
        iframe_xpath = IFRAME_PATHS.get(key)
        if not iframe_xpath:
            raise ValueError(f"등록되지 않은 iframe 키입니다: {key}")

        iframe_elem = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe_elem)
        logger.info(f"✅ iframe 전환 성공 → {key} ({iframe_xpath})")
        return True
    except NoSuchElementException:
        logger.error(f"❌ iframe 요소를 찾을 수 없습니다: {key}")
        return False
    except Exception as e:
        logger.exception(f"❌ iframe 전환 실패 ({key}): {e}")
        raise

# 관리자 저장/등록/수정 버튼
def save_data(driver, timeout: int = 8) -> bool:
    """
    [간단 버전] 저장/등록/수정 버튼 클릭 후 확인(알럿/모달)까지 처리.
    1) 'fn_save*' onclick 또는 라벨(저장/등록/수정)로 액션 버튼 클릭
    2) 브라우저 알럿(confirm/alert)이면 switch_to.alert 로 수락
    3) 아니면 화면 모달(HTML)에서 [확인](id=saveBtn 또는 텍스트) 클릭
       - 가려져 있으면 JS click으로 재시도
    4) 그래도 안 되면 window.fn_save() 직접 호출(있을 때)
    5) 추가 알럿/모달이 없는 경우도 정상 종료로 처리
    """
    log = logging.getLogger(__name__)

    # 1) 저장/등록/수정 버튼 클릭
    action_xpath = (
        "//button[contains(@onclick,'fn_save')] | //a[contains(@onclick,'fn_save')] | "
        "//button[contains(.,'저장') or contains(.,'등록') or contains(.,'수정')] | "
        "//a[contains(.,'저장') or contains(.,'등록') or contains(.,'수정')]"
    )
    btn = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, action_xpath))
    )
    try:
        btn.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        driver.execute_script("arguments[0].click();", btn)
    time.sleep(0.2)

    # 2) 브라우저 알럿 우선 처리
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        txt = (alert.text or "").strip()
        alert.accept()
        log.info(f"[save_data] 브라우저 알럿 수락: {txt}")
        return True
    except Exception:
        pass

    # 3) 화면 모달(HTML) 확인 버튼 처리
    modal_xpath = ("//div[contains(@class,'modal') or contains(@class,'layer')]"
                   "[not(contains(@style,'display: none'))]")
    try:
        modal = WebDriverWait(driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, modal_xpath))
        )
        try:
            ok = modal.find_element(By.ID, "saveBtn")
        except Exception:
            ok = modal.find_element(
                By.XPATH, ".//button[normalize-space()='확인' or normalize-space()='OK' or normalize-space()='예']"
            )
        try:
            ok.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ok)
            driver.execute_script("arguments[0].click();", ok)
        return True
    except TimeoutException:
        pass

    # 4) 최후수단: 화면 저장 함수 직접 호출
    try:
        exists = driver.execute_script("return typeof window.fn_save === 'function';")
        if exists:
            driver.execute_script("window.fn_save();")
            log.info("[save_data] window.fn_save() 직접 호출")
            return True
    except Exception:
        pass

    # ✅ 5) 추가 알럿/모달이 없는 경우도 정상 종료로 처리
    log.info("[save_data] 추가 알럿/모달 없음 — 저장 완료로 간주")
    return True


# 통합 폼 필드 처리 함수
def fill_form_field(driver, wait, selector: str, value=None, *, field_type=None, checked=True, timeout=5, ui_name=None):
    """
    ✅ 통합 폼 필드 처리 함수 (Text / Select / Checkbox / Radio / Click / File 자동 인식)
    selector : id, class, xpath, name 모두 지원 (#, ., //, name=)
    field_type : 'auto' | 'select' | 'checkbox' | 'radio' | 'text' | 'click' | 'file'
    """
    label = ui_name or selector
    try:
        # ─────────────────────────────
        # 1️⃣ 요소 탐색 (selector 인식)
        # ─────────────────────────────
        if selector.startswith("//"):
            element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        elif selector.startswith("#") or selector.startswith("."):
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elif selector.startswith("name="):
            name_val = selector.split("=", 1)[1]
            element = wait.until(EC.presence_of_element_located((By.NAME, name_val)))
        else:
            try:
                element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            except Exception:
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, selector)))

        tag = element.tag_name.lower()
        html = element.get_attribute("outerHTML")

        # ─────────────────────────────
        # 2️⃣ 타입 자동 판별
        # ─────────────────────────────
        if not field_type or field_type == "auto":
            if "nice-select" in html or "selectbox" in html:
                field_type = "select"
            elif "checkbox" in html:
                field_type = "checkbox"
            elif "radio" in html:
                field_type = "radio"
            elif "type=\"file\"" in html:
                field_type = "file"
            elif tag in ["input", "textarea"]:
                field_type = "text"
            elif "button" in tag or "onclick" in html:
                field_type = "click"
            else:
                raise ValueError(f"자동판별 실패: {selector}")

        logger.info(f"🎯 필드 타입 인식 → {field_type} ({label})")

        # ─────────────────────────────
        # 3️⃣ 타입별 처리
        # ─────────────────────────────
        # ✅ Text 입력
        if field_type == "text":
            element.clear()
            element.send_keys(value)
            logger.info(f"✅ {label} 입력 완료: {value}")

        # ✅ Select (nice-select / 일반 select)
        elif field_type == "select":
            try:
                if "nice-select" in element.get_attribute("class"):
                    click(driver, element)
                    time.sleep(0.3)
                    options = driver.find_elements(By.CSS_SELECTOR, ".nice-select.open .option")
                    for opt in options:
                        text, val = opt.text.strip(), (opt.get_attribute("data-value") or "").strip()
                        if value.strip() in (text, val):
                            click(driver, opt)
                            logger.info(f"✅ {label} '{text}' 선택 완료")
                            break
                    else:
                        raise Exception(f"'{value}' 옵션을 찾을 수 없습니다.")
                else:
                    from selenium.webdriver.support.ui import Select
                    Select(element).select_by_visible_text(value)
                    logger.info(f"✅ {label} '{value}' 선택 완료 (일반 select)")
            except Exception as e:
                logger.error(f"❌ {label} select 처리 실패: {e}")
                raise

        # ✅ Checkbox
        elif field_type == "checkbox":
            values = value if isinstance(value, list) else [value] if value else []
            for v in values:
                try:
                    label_xpath = f".//label[normalize-space(text())='{v}']"
                    label_el = element.find_element(By.XPATH, label_xpath)
                    checkbox_el = label_el.find_element(By.XPATH, "./preceding-sibling::input[@type='checkbox']")
                    is_checked = checkbox_el.is_selected()

                    # ✅ scrollIntoView 복구 (뷰포트 정렬용)
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label_el)

                    if checked and not is_checked:
                        click(driver, label_el)
                        logger.info(f"✅ {label} '{v}' 체크 완료")
                    elif not checked and is_checked:
                        click(driver, label_el)
                        logger.info(f"✅ {label} '{v}' 해제 완료")
                except Exception:
                    # ✅ fallback에도 scroll 추가
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                    click(driver, element)
                    logger.warning(f"⚠ '{v}' 라벨 없음, 직접 클릭 수행")
                time.sleep(0.2)

            # ✅ 단일 체크형 복구
            if not values:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                click(driver, element)
                logger.info(f"✅ {label} 체크박스 직접 클릭 완료 (value 없음)")
                time.sleep(0.3)

        # ✅ Radio
        elif field_type == "radio":
            val_target = (value or "").strip()
            radios = driver.find_elements(By.CSS_SELECTOR, f"input[type='radio']")
            for r in radios:
                rv = (r.get_attribute("value") or "").strip()
                if rv == val_target:
                    click(driver, r)
                    logger.info(f"✅ {label} '{value}' 선택 완료")
                    break
            else:
                logger.warning(f"⚠ {label}: '{value}' 라디오 옵션을 찾을 수 없습니다.")

        # ✅ Click (버튼)
        elif field_type == "click":
            click(driver, element)
            logger.info(f"✅ {label} 클릭 완료")

        # ✅ File 업로드
        elif field_type == "file":
            scroll_into_view(driver, element)
            if not os.path.exists(value):
                raise FileNotFoundError(value)
            element.send_keys(value)
            logger.info(f"✅ {label} 업로드 완료 → {os.path.basename(value)}")

        # ✅ 기타
        else:
            raise ValueError(f"지원하지 않는 field_type: {field_type}")

    except Exception as e:
        logger.exception(f"❌ fill_form_field({label}) 처리 중 오류: {e}")
        raise

# 등록 버튼 클릭
def submit(driver, wait, iframe_key="asIsAdmin"):
    try:
        switch_iframe(driver, iframe_key)
        driver.find_element(By.CSS_SELECTOR, "a.btn.btn_xs.fill_primary").click()
        time.sleep(1)
        logger.info("등록 버튼 클릭 성공")
        return True
    except Exception as e:
        logger.exception(f"등록 버튼 클릭 실패: {e}")
        raise

# ======================================
# 공통: LNB 탐색
# ======================================
def navigation(driver, wait, L_menu: str, M_menu: str = None, S_menu: str = None, L_index=0, M_index=0, S_index=0):
    """
    [공통] 관리자 페이지 좌측 메뉴 네비게이션 (L → M → S 자동 인식)
    ------------------------------------------------------------
    사용처:
        - Giftian 관리자
        - 오투어 관리자
        - 복지몰 관리자 등
    ------------------------------------------------------------
    인자 설명:
        L_menu: 1단계 메뉴명 (필수)
        M_menu: 2단계 메뉴명 (선택)
        S_menu: 3단계 메뉴명 (선택)
        L_index/M_index/S_index: 동일 메뉴명이 여러 개 있을 때 인덱스로 구분
    ------------------------------------------------------------
    예시:
        navigation(driver, wait, "회원관리", "회원관리")
        navigation(driver, wait, "정산관리", "정산내역", "월별 정산")
    """
    try:
        # 1️⃣ L 메뉴 클릭
        wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, L_menu)))
        L_menus = driver.find_elements(By.LINK_TEXT, L_menu)
        if len(L_menus) <= L_index:
            raise Exception(f"'{L_menu}' 메뉴({L_index})를 찾을 수 없습니다.")
        
        L_menu_element = L_menus[L_index]
        click(driver, L_menu_element)
        time.sleep(1)
        logger.info(f"✅ 1단 메뉴 클릭 완료 → {L_menu}")

        # 2️⃣ M 메뉴 (있을 경우) - 하위 메뉴 컨테이너에서만 검색
        if M_menu:
            # L 메뉴의 부모/형제 요소에서 하위 메뉴 찾기
            try:
                # 방법 1: 열린 하위 메뉴 영역에서만 검색 (class에 'open', 'active', 'on' 등 포함)
                sub_menu_container = L_menu_element.find_element(
                    By.XPATH, 
                    "./following-sibling::ul | ./parent::*/following-sibling::ul | ./parent::*/ul"
                )
                M_menus = sub_menu_container.find_elements(By.LINK_TEXT, M_menu)
            except:
                # 방법 2: 전체에서 검색하되, L 메뉴는 제외
                all_M_menus = driver.find_elements(By.LINK_TEXT, M_menu)
                M_menus = [m for m in all_M_menus if m != L_menu_element]
            
            if len(M_menus) <= M_index:
                raise Exception(f"'{M_menu}' 메뉴({M_index})를 찾을 수 없습니다.")
            
            M_menu_element = M_menus[M_index]
            click(driver, M_menu_element)
            time.sleep(0.5)
            logger.info(f"✅ 2단 메뉴 클릭 완료 → {L_menu} > {M_menu}")

        # 3️⃣ S 메뉴 (있을 경우)
        if S_menu:
            if M_menu:
                # M 메뉴의 하위에서 검색
                try:
                    sub_menu_container = M_menu_element.find_element(
                        By.XPATH, 
                        "./following-sibling::ul | ./parent::*/following-sibling::ul | ./parent::*/ul"
                    )
                    S_menus = sub_menu_container.find_elements(By.LINK_TEXT, S_menu)
                except:
                    all_S_menus = driver.find_elements(By.LINK_TEXT, S_menu)
                    S_menus = [s for s in all_S_menus if s != M_menu_element and s != L_menu_element]
            else:
                S_menus = driver.find_elements(By.LINK_TEXT, S_menu)
            
            if len(S_menus) <= S_index:
                raise Exception(f"'{S_menu}' 메뉴({S_index})를 찾을 수 없습니다.")
            click(driver, S_menus[S_index])
            time.sleep(0.5)
            logger.info(f"✅ 3단 메뉴 클릭 완료 → {L_menu} > {M_menu} > {S_menu}")

        logger.info(f"🎯 메뉴 이동 성공: {L_menu} > {M_menu if M_menu else '-'} > {S_menu if S_menu else '-'}")
        return True

    except Exception as e:
        logger.exception(f"❌ navigation 실패: {e}")
        raise


def set_usage_radio(driver, wait, value: str):
    """
    사용여부 라디오 버튼 선택
    :param driver: WebDriver 인스턴스
    :param wait: WebDriverWait 인스턴스
    :param value: 'Y' 또는 'N'
    """
    value = value.upper()
    if value not in ["Y", "N"]:
        raise ValueError("value must be 'Y' or 'N'")

    try:
        radio_id = "useOk" if value == "Y" else "useNo"
        element = wait.until(EC.element_to_be_clickable((By.ID, radio_id)))
        driver.execute_script("arguments[0].click();", element)
        label = "사용" if value == "Y" else "미사용"
        logger.info(f"✅ '{label}' 라디오 버튼 선택 완료")
        return True
    except Exception as e:
        logger.exception(f"❌ 사용여부 선택 중 오류 발생: {e}")
        raise

# 자동화 일시 정지
def wait_for_user_input(prompt="결제 완료 후 확인 버튼을 눌러주세요."):
    pyautogui.alert(prompt, title="🟢 결제 수동 진행 중")
    logger.info("✅ GUI 창에서 확인 입력 → 자동화 재개")








