import logging, os, pyautogui, sys, time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # setup
from munhak.module.setup_common_functions import (setup_driver)
    # admin
from munhak.module.admin_common_functions import (
    admin_login, site_management_tab, iframe, inquiry_register, answer_inquiry, save_inquiry,generate_date_range)
    # homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, some_function)
    # dokpa
from munhak.module.dokpa_common_functions import (
    dokpa_enter, some_function, my_dokpa, my_dokpa_setting, my_dokpa_one_on_one)

def main():
    driver, wait = setup_driver()
    some_function()
    # 날짜 지정 함수 호출
    date_info = generate_date_range(min_days=-1, max_days=3)
    start_date = date_info['start_date']
    dates_list = date_info['dates_list']
    # 관리자 url, 계정
    admin_homepage_url = "https://dev-munhak-manager.ntoday.kr/login"
    admin_id = "soyeonkim01"
    admin_pw = "7$f41OpW"
    # 홈페이지 url, 계정
    homepage_url = "https://dev-munhak-home.ntoday.kr/"
    user_id = "seoha40@ntoday.kr"
    user_pw = "admin123"

    # 문학동네 홈페이지 진입
    try:
        home_page(driver, wait, homepage_url)
        print("문학동네 홈페이지 진입 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"문학동네 홈페이지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
    # 로그인
    try:
        munhak_login(driver, wait, user_id, user_pw)
        print("로그인 성공")
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 독파 진입
    try:
        dokpa_enter(driver, wait)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        print("독파 진입 성공")
    except Exception as e:
        logging.error(f"독파 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 마이독파
    try:
        my_dokpa(driver, wait)
        print("마이독파 진입 성공")
    except Exception as e:
        logging.error(f"마이독파 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 마이독파 > 설정
    try:
        my_dokpa_setting(driver,wait)
        print("마이독파 설정 진입 성공")
    except Exception as e:
        logging.error(f"마이독파 설정 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 1:1 문의
    try:
        inquiry_title_value = "문의 테스트1"
        inquiry_detail_value = "문의 상세 입력"
        my_dokpa_one_on_one(driver,wait, inquiry_title_value, inquiry_detail_value)
        print("1:1문의 작성 성공")
    except Exception as e:
        logging.error(f"1:1문의 작성 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 관리자 로그인
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        admin_login(driver,admin_homepage_url, admin_id, admin_pw)
        print("관리자 로그인 성공")
    except Exception as e:
        logging.error(f"관리자 로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 관리자 > 사이트 관리 탭 진입
    try:
        site_management_tab(driver, wait)
        print("관리자 > 사이트 관리 진입 성공")
    except Exception as e:
        logging.error(f"관리자 > 사이트 관리 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 관리자 > 사이트관리 > 문의관리 진입
    try:
        iframe(driver, wait)
        inquiry_register(driver, wait, inquiry_title_value)
        print("관리자 > 사이트관리 > 문의관리 진입 성공")
    except Exception as e:
        logging.error(f"관리자 > 사이트관리 > 문의관리 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 관리자 > 문의 답변 입력
    try:
        answer_inquiry_value = "문의 답변 테스트 01" # 문의 답변 입력
        answer_inquiry(driver,wait, answer_inquiry_value)
        print("문의 답변 입력 성공")
    except Exception as e:
        logging.error(f"문의 답변 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 관리자 > 문의 저장
    try:
        driver.switch_to.default_content()
        iframe(driver, wait)
        save_inquiry(driver, wait)
        print("문의 저장 성공")
    except Exception as e:
        logging.error(f"문의 저장 테스트 중 오류가 발생했습니다: {str(e)}")
        return

    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()
