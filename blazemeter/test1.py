# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import unittest

class MailTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://ntoday.daouoffice.com/login"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_send_mail_to_self(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)

        # 1. 로그인 페이지 접속
        driver.get(self.base_url)
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("seoha.lee@ntoday.kr")
        # 2. 비밀번호 입력 (ID는 자동입력이라 가정)
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("rhaoddl1143!")

        # 3. 로그인
        driver.find_element(By.ID, "loginForm").submit()

        # 4. '메일' 메뉴 클릭
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, u"메일"))).click()

        # 5. 특정 메일 클릭 (예시 메일 제목 일부 일치)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-preview*="하나투어"]'))).click()

        # 6. 메일 제목 클릭
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.txt"))).click()

        # 7. 본인에게 다시 보내기 클릭
        driver.find_element(By.ID, "writeMyself").click()

        # 8. 제목 수정
        subject = wait.until(EC.presence_of_element_located((By.ID, "subject")))
        subject.clear()
        subject.send_keys("test")

        # 9. 전송 버튼 클릭
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_major_s > span.txt"))).click()

        # 10. 전송 확인 (모달 버튼 등)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "footer.btn_layer_wrap > a.btn_major_s > span.txt"))).click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
            return True
        except NoSuchElementException:
            return False

    def is_alert_present(self):
        try:
            _ = self.driver.switch_to.alert.text
            return True
        except NoAlertPresentException:
            return False

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
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
