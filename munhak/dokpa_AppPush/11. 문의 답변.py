import logging, pyautogui
    # setup
from n2common.web.setup_module import (setup_driver, get_current_dir, get_parent_dir)
    # admin
from module.admin_common_functions import (
    admin_login, site_management_tab, iframe, inquiry_register, answer_inquiry, answerYN, save_inquiry)
    # homepage
from module.homepage_common_functions import (
    home_page, munhak_login)
    # dokpa
from module.dokpa_common_functions import (
    dokpa_enter, my_dokpa, my_dokpa_setting, my_dokpa_one_on_one)

# log
logger = logging.getLogger()
# path
current_dir = get_current_dir()
parent_dir = get_parent_dir(2)

def main():
    driver, wait = setup_driver()

    # 문학동네 홈페이지 진입
    home_page(driver, wait)

    # 문학동네 로그인
    munhak_login(driver, wait, "seoha40@ntoday.kr", "admin123")

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
    admin_login(driver, "soyeonkim01", "7$f41OpW")

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
