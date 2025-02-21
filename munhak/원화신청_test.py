# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import unittest, time, re

class Record02042543346Pm(unittest.TestCase):
    def setUp(self):
        # 크롬 드라이버 설정
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # service = Service('/path/to/chromedriver')  # Service 객체 사용
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(30)
        # self.base_url = "https://www.blazedemo.com/"
        self.driver.maximize_window()
    
    def test_record02042543346_pm(self):
        driver = self.driver
        # 웹사이트 열기
        driver.get("https://dev-munhak-home.ntoday.kr/")
        # 요소 클릭
        # driver.find_element(By.CSS_SELECTOR, "div.main_sec.main_sec01").click()
        # driver.find_element(By.CSS_SELECTOR, "div.main_sec.main_sec01").click()
        driver.find_element(By.CSS_SELECTOR, "span.tooltip").click()
        # 사용자 ID 입력
        # driver.find_element(By.ID, "userId").clear()
        # driver.find_element(By.ID, "userId").send_keys("admin123")
        # driver.find_element(By.ID, "contents").click()
        driver.find_element(By.ID, "userId").clear()
        driver.find_element(By.ID, "userId").send_keys("soyeon.kim@ntoday.kr")
        # 로그인 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "button.btn.fill_black").click()
        # 메뉴 클릭
        driver.find_element(By.CSS_SELECTOR, "li:nth-of-type(4) .hover").click()
        driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(9) .txt").click()
        driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(4) > label > span").click()
        # 조직 입력
        driver.find_element(By.ID, "organization").click()
        driver.find_element(By.ID, "organization").clear()
        driver.find_element(By.ID, "organization").send_keys(u"소연기관")
        # 체크박스 클릭
        driver.find_element(By.CSS_SELECTOR, "div.checkbox.txt > label > span").click()
        # 제출 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "button.btn.fill_black.false").click()
        driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(4) .btn").click()
    
    def is_element_present(self, how, what):
        try: 
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: 
            return False
        return True
    
    def is_alert_present(self):
        try: 
            self.driver.switch_to.alert
        except NoAlertPresentException as e: 
            return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: 
            self.accept_next_alert = True
    
    def tearDown(self):
        # 드라이버 종료
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
if __name__ == "__main__":
    unittest.main(exit=False)
