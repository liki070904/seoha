import logging, os, pyautogui, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # setup
from munhak.module.setup_common_functions import (setup_driver)
    # admin
from munhak.module.admin_common_functions import (
    admin_login, site_management_tab, iframe, inquiry_register, answer_inquiry, answerYN, save_inquiry)
    # homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login)
    # dokpa
from munhak.module.dokpa_common_functions import (
    dokpa_enter, my_dokpa, my_dokpa_setting, my_dokpa_one_on_one)
logger = logging.getLogger()

# 관리자 url, 계정
admin_homepage_url = "https://dev-munhak-manager.ntoday.kr/login"
admin_id = "soyeonkim01"
admin_pw = "7$f41OpW"
# 홈페이지 url, 계정
homepage_url = "https://dev-munhak-home.ntoday.kr/"
user_id = "seoha40@ntoday.kr"
user_pw = "admin123"

def main():
    driver, wait = setup_driver()

    # 문학동네 홈페이지 진입
    home_page(driver, wait, homepage_url)

    # 문학동네 로그인
    munhak_login(driver, wait, user_id, user_pw)

    # 독파 진입 및 팝업 닫기 함수
    dokpa_enter(driver, wait)
    driver.switch_to.window(driver.window_handles[1])

    # 마이독파
    my_dokpa(driver, wait)

    # 마이독파 > 설정
    my_dokpa_setting(driver,wait)

    # 마이독파 > 1:1 문의
    inquiry_title_value = "문의 테스트1"
    inquiry_detail_value = "문의 상세 입력"
    my_dokpa_one_on_one(driver,wait, inquiry_title_value, inquiry_detail_value)

    # 관리자 로그인
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    admin_login(driver,admin_homepage_url, admin_id, admin_pw)

    # 관리자 > 사이트 관리 탭 진입
    site_management_tab(driver, wait)

    # 관리자 > 사이트관리 > 문의관리 진입
    iframe(driver, wait)
    inquiry_register(driver, wait, inquiry_title_value)

    # 관리자 > 문의 답변 입력
    answer_inquiry_value = "문의 답변 테스트 01" # 문의 답변 입력
    answer_inquiry(driver,wait, answer_inquiry_value)

    # 관리자 > 문의 > 답변여부 변경
    answerYN(driver,wait)

    # 관리자 > 문의 저장
    save_inquiry(driver, wait)

    # test_exit
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()
