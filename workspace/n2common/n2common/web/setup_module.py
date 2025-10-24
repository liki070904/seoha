import pyautogui, os, time, logging, re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import tkinter as tk

logger = logging.getLogger(__name__)

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
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# 스크롤 최하단으로
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
            print("팝업 닫기 완료")
        else:
            print("팝업이 존재하지 않습니다.")
    except Exception as e:
        print(f"팝업 닫기 중 오류 발생: {e}")
# 얼럿 내용 확인 O 닫기
def check_html_alert_text(driver, expected_text=None, timeout=5):
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
# 얼럿 내용 확인 X 닫기
def accept_basic_alert(driver, timeout=3):
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

# iframe 이동
def iframe(driver, wait):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)

# 복지몰 취소요청 조회 iframe
def cancel_iframe(driver, wait):
    cancel_iframe_switch = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[4]/div/iframe')
    driver.switch_to.frame(cancel_iframe_switch)

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
    -----------------------------------------------------------------------------
    selector : id, class, xpath, name 모두 지원 (#, ., //, name=)
    value    : 입력 또는 선택할 값 (checkbox는 list 가능)
    field_type : 'auto' | 'select' | 'checkbox' | 'radio' | 'text' | 'click' | 'file'
    checked  : checkbox용 → True = 선택, False = 해제
    ui_name  : (선택) UI 항목명 (로그 표시용)
    timeout  : 대기 시간 (기본 5초)
    -----------------------------------------------------------------------------
    예시:
        fill_form_field(driver, wait, "#checkbox_area", ["오투어"], field_type="checkbox", ui_name="이용동의")
        fill_form_field(driver, wait, "//button[normalize-space(text())='로그인']", None, field_type="click", ui_name="로그인 버튼")
    """
    try:
        label = ui_name or selector

        # ✅ selector 자동 인식
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

        # ✅ 타입 자동 판별
        if not field_type or field_type == "auto":
            if "nice-select" in html or "selectbox" in html:
                field_type = "select"
            elif "checkbox" in html or "checkbox_area" in html:
                field_type = "checkbox"
            elif "radio" in html or "radio_area" in html:
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

        # ✅ 1️⃣ Text 입력
        if field_type == "text":
            element.clear()
            element.send_keys(value)
            logger.info(f"✅ {label} 입력 완료: {value}")

        # ✅ 2️⃣ Nice Select / 일반 Select 처리
        elif field_type == "select":
            try:
                if "nice-select" in element.get_attribute("class"):
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                    click(driver, element)
                    time.sleep(0.3)

                    options = driver.find_elements(By.CSS_SELECTOR, ".nice-select.open .option")
                    found = False
                    for opt in options:
                        opt_text = opt.text.strip()
                        opt_val = (opt.get_attribute("data-value") or "").strip()
                        if value.strip() == opt_text or value.strip() == opt_val:
                            click(driver, opt)
                            logger.info(f"✅ {label} '{opt_text}' 선택 완료")
                            found = True
                            break

                    if not found:
                        raise Exception(f"'{value}' 옵션을 찾을 수 없습니다 ({selector})")

                else:
                    from selenium.webdriver.support.ui import Select
                    Select(element).select_by_visible_text(value)
                    logger.info(f"✅ {label} '{value}' 선택 완료 (일반 select)")

            except Exception as e:
                logger.error(f"❌ {label} select 처리 실패 ({selector}) → {e}")
                raise

        # ✅ 3️⃣ Checkbox
        elif field_type == "checkbox":
            try:
                # ① 리스트/단일 값 처리
                values = value if isinstance(value, list) else [value] if value else []

                # ② label 기준 (일반 다중체크 형태)
                if values:
                    for v in values:
                        try:
                            label_xpath = f".//label[normalize-space(text())='{v}']"
                            label_el = element.find_element(By.XPATH, label_xpath)
                            checkbox_el = label_el.find_element(By.XPATH, "./preceding-sibling::input[@type='checkbox']")
                            is_checked = checkbox_el.is_selected()

                            if checked and not is_checked:
                                click(driver, label_el)
                                logger.info(f"✅ {label} '{v}' 체크 완료")
                            elif not checked and is_checked:
                                click(driver, label_el)
                                logger.info(f"✅ {label} '{v}' 해제 완료")
                            else:
                                logger.info(f"⚪ {label} '{v}' 이미 올바른 상태 유지 중")

                        except Exception:
                            logger.warning(f"⚠ '{v}' 라벨 탐색 실패, input 직접 클릭 시도")
                            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                            click(driver, element)
                            logger.info(f"✅ {label} 직접 클릭 완료 (라벨 미존재)")
                        time.sleep(0.2)

                # ③ value=None → input id 직접 클릭 (단일 체크형)
                else:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                    click(driver, element)
                    logger.info(f"✅ {label} 체크박스 직접 클릭 완료 (value 없음)")
                    time.sleep(0.3)

            except Exception as e:
                logger.error(f"❌ {label} 체크박스 처리 실패 ({selector}) → {e}")
                raise

        # ✅ 4️⃣ Radio
        elif field_type == "radio":
            try:
                val_raw = (value or "").strip()
                target_val = val_raw

                if selector.strip().startswith("//"):
                    radios = driver.find_elements(By.XPATH, selector)
                else:
                    radios = driver.find_elements(By.CSS_SELECTOR, selector)

                for r in radios:
                    rv = (r.get_attribute("value") or "").strip()
                    if rv == target_val:
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", r)
                        click(driver, r)
                        logger.info(f"✅ {label} '{value}' 선택 완료")
                        return

                labels = driver.find_elements(By.CSS_SELECTOR, "label")
                for lbl in labels:
                    if (lbl.text or "").strip().replace(" ", "") == val_raw.replace(" ", ""):
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", lbl)
                        click(driver, lbl)
                        logger.info(f"✅ {label} '{value}' 선택 완료 (라벨)")
                        return

                raise Exception(f"'{value}' 라디오 옵션을 찾을 수 없습니다 ({selector})")

            except Exception as e:
                logger.error(f"❌ {label} 라디오 버튼 선택 실패 ({selector}) → {e}")
                raise

        # ✅ 5️⃣ Click
        elif field_type == "click":
            click(driver, element)
            logger.info(f"✅ {label} 클릭 완료")

        # ✅ 6️⃣ File 업로드
        elif field_type == "file":
            try:
                if selector.startswith("//"):
                    file_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                else:
                    file_input = wait.until(EC.presence_of_element_located((By.ID, selector)))

                # driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
                scroll_into_view(driver, file_input)
                time.sleep(0.3)

                if not os.path.exists(value):
                    raise FileNotFoundError(value)

                file_input.send_keys(value)
                time.sleep(1)

                logger.info(f"✅ {label} 업로드 완료 → {os.path.basename(value)}")

            except Exception as e:
                logger.error(f"❌ {label} 업로드 실패 ({selector}) → {e}")
                raise

    except Exception as e:
        logger.exception(f"❌ fill_form_field({label}) 처리 중 오류 발생: {e}")
        raise

# 등록 버튼 클릭
def submit(driver, wait):
    """목록 화면에서 '등록' 버튼 클릭 (새 등록 화면으로 진입)."""
    try:
        iframe(driver, wait)
        driver.find_element(By.CSS_SELECTOR, "a.btn.btn_xs.fill_primary").click()
        time.sleep(1)
        logger.info("등록 버튼 클릭 성공")
        return True
    except Exception as e:
        logger.exception(f"등록 버튼 클릭 실패: {e}")
        raise


# ======================================
# 공통: 좌측 메뉴 탐색
# ======================================
def navigation(driver, L_menu: str, M_menu: str, S_menu: str, L_index=0, M_index=0, S_index=0):
    """
    [공통] 좌측 메뉴 L→M→S 순서로 클릭 후 iframe 진입
    사용처:
        - Giftian 관리자
        - 오투어 관리자
        - 복지몰 관리자 등
    """
    from n2common.web.setup_module import click
    try:
        # 1️⃣ L 메뉴 클릭
        L_menus = driver.find_elements(By.LINK_TEXT, L_menu)
        if len(L_menus) <= L_index:
            raise Exception(f"'{L_menu}' 메뉴({L_index})를 찾을 수 없습니다.")
        click(driver, L_menus[L_index])
        time.sleep(0.5)

        # 2️⃣ M 메뉴 클릭
        M_menus = driver.find_elements(By.LINK_TEXT, M_menu)
        if len(M_menus) <= M_index:
            raise Exception(f"'{M_menu}' 메뉴({M_index})를 찾을 수 없습니다.")
        click(driver, M_menus[M_index])
        time.sleep(0.5)

        # 3️⃣ S 메뉴 클릭
        S_menus = driver.find_elements(By.LINK_TEXT, S_menu)
        if len(S_menus) <= S_index:
            raise Exception(f"'{S_menu}' 메뉴({S_index})를 찾을 수 없습니다.")
        click(driver, S_menus[S_index])
        time.sleep(0.5)

        logger.info(f"✅ 메뉴 이동 완료 → {L_menu} > {M_menu} > {S_menu}")
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
def wait_for_user_input_gui(prompt="결제 완료 후 확인 버튼을 눌러주세요."):
    pyautogui.alert(prompt, title="🟢 결제 수동 진행 중")
    logger.info("✅ GUI 창에서 확인 입력 → 자동화 재개")










