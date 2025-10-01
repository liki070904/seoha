# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Record032125111647Am(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.blazedemo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_record032125111647_am(self):
        driver = self.driver
        # Label: Test
        # ERROR: Caught exception [ERROR: Unsupported command [resizeWindow | 2560,911 | ]]
        driver.get("https://ntoday.daouoffice.com/login")
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID,"username").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "username").clear()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "username").send_keys("seoha.lee@ntoday.kr")
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "password").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys("rhaoddl1143!")
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "loginForm").submit()
        # ERROR: Caught exception [unknown command [waitFor]]
        # ERROR: Caught exception [unknown command [typeSecret]]
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.LINK_TEXT, u"메일").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | id=mail-viewer | ]]
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, u"[data-preview=\"하나투어 &#58;&#58; 1등 여행사 (주)하나투어 여행계약서 동의 안내 고객님께서 예약하신 ATX700250615006 상품의 여행계약서입니다. 여행계약서 내용을 확인하시고 동의하여 주시기 바랍니다. 기타\"]").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, u"[data-preview=\"하나투어 &#58;&#58; 1등 여행사 (주)하나투어 여행계약서 동의 안내 고객님께서 예약하신 AAP200250601BXA 상품의 여행계약서입니다. 여행계약서 내용을 확인하시고 동의하여 주시기 바랍니다. 기타\"]").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "span.txt").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "#mailWriteAreaTable > tbody > tr > th > span.title").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "writeMyself").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "subject").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.ID, "subject").clear()
        driver.find_element(By.ID, "subject").send_keys("test")
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "a.btn_major_s > span.txt").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "footer.btn_layer_wrap > a.btn_major_s > span.txt").click()
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(2) > a:nth-of-type(3) > .txt").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, "[data-menu=\"mail\"] .menu").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | id=mail-viewer | ]]
        # ERROR: Caught exception [unknown command [waitFor]]
        driver.find_element(By.CSS_SELECTOR, u"[data-preview=\"              (주)엔투솔루션   이서하  주임 대외 SI사업 본부 / 품질관리팀   Mobile &#58; 010-2207-7353 Tel &#58; 02-2088-4797 E-mail &#58; seoha.lee @ntoday.kr   website &#58;\"]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert
        except NoAlertPresentException as e: return False
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
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
