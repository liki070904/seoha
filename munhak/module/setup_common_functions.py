from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

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