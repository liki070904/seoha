from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os, time, logging, threading
import tkinter as tk
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

    # WebDriver 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 대기 설정
    driver.implicitly_wait = (10)
    wait = WebDriverWait(driver, 10)
    return driver, wait
# 요소가 보이는 영역 안에 있도록 스크롤하는 함수
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# 스크롤 최하단으로
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 클릭
def click(driver, element):
    driver.execute_script("arguments[0].click();", element)
# iframe
def iframe(driver):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)
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
    toast_width = 400
    toast_height = 80

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
# 오투어 예약조회 iframe
def iframe(driver, wait):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)
# 복지몰 취소요청 조회 iframe
def cancel_iframe(driver, wait):
    cancel_iframe_switch = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[4]/div/iframe')
    driver.switch_to.frame(cancel_iframe_switch)
