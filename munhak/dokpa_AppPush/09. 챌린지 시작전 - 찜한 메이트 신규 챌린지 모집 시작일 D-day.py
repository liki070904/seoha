import logging, os, pyautogui, sys, time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # setup
from munhak.module.setup_common_functions import (setup_driver)
    # admin
from munhak.module.admin_common_functions import (
    admin_login, choice_book, challenge_detail, Recruitment_period, challenge_period, search_mate, challenge_save,
    generate_date_range, challenge_tab, challenge_register)
    # homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, some_function)
    # dokpa
from munhak.module.dokpa_common_functions import (
    dokpa_enter, some_function, all_challenge_apply, myBookmark_mate, same_challenge_name_value)

def main():
    driver, wait = setup_driver()
    some_function()
    # 날짜 지정 함수 호출
    date_info = generate_date_range(min_days=0, max_days=3)
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

    try:
        admin_login(driver, admin_homepage_url, admin_id, admin_pw)
        print("관리자 로그인 성공")
        time.sleep(2)
    except Exception as e:
        logging.error(f"관리자 로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        challenge_tab(driver,wait)
        print("챌린지 탭 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 탭 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        challenge_register(driver, wait)
        print("챌린지 탭 등록 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"챌린지 탭 등록 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        book_name_value = "해리" # 도서명 검색
        challenge_name_value = "서하 자동화 테스트 - 찜한 메이트 신규 모집 시작 01" # 챌린지명 입력
        choice_book(driver, wait, challenge_name_value, book_name_value)
        print("도서 선택 & 챌린지 명 입력 성공")
    except Exception as e:
        logging.error(f"도서 선택 & 챌린지 명 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        challenge_detail_value = "서하 자동화 테스트 상세 설명" # 챌린지 상세설명 입력
        challenge_detail(driver, wait, challenge_detail_value)
        print("챌린지 상세 입력 성공")
    except Exception as e:
        logging.error(f"챌린지 상세 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:   #현재월 : 1 / 다음월 : 2 / 오늘(start_index) : 0 / 내일(end_index) : 1
        start_index, end_index = 0,0
        Recruitment_period(driver, wait, dates_list, start_index, end_index, 1, 1)
        print("모집 기간 설정 완료")
    except Exception as e:
        logging.error(f"모집 기간 설정 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:   #현재월 : 1 / 다음월 : 2 / 오늘(start_index) : 0 / 내일(end_index) : 1
        start_index, end_index = 1,1
        challenge_period(driver, wait, dates_list, start_index, end_index, 1, 1)
        print("챌린지 기간 설정 완료")
    except Exception as e:
        logging.error(f"챌린지 기간 설정 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        mate_name_value = "서하" # 메이트명 검색
        search_mate(driver, wait, mate_name_value, "서하 통합 계정")  # 선택할 메이트 닉네임
        print("메이트 설정 완료")
    except Exception as e:
        logging.error(f"메이트 설정 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        challenge_save(driver, wait)
        print("챌린지 저장 완료")
    except Exception as e:
        logging.error(f"챌린지 저장 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        home_page(driver, wait, homepage_url)
        print("문학동네 홈페이지 진입 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"문학동네 홈페이지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        munhak_login(driver, wait, user_id, user_pw)
        print("로그인 성공")
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        dokpa_enter(driver, wait)
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(2)
        print("독파 진입 성공")
    except Exception as e:
        logging.error(f"독파 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        all_challenge_apply(driver, wait)
        print("챌린지 전체 탭 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 전체 탭 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        same_challenge_name_value(driver, wait, challenge_name_value)
        print("챌린지 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        myBookmark_mate(driver, wait)
        print("메이트 찜하기 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"메이트 찜하기 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.default_content()
        print("관리자 페이지로 전환 성공")
    except Exception as e:
        logging.error(f"관리자 페이지 전환 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    try:
        challenge_register(driver,wait)
        challenge_name_value = "서하 자동화 테스트 - 찜한 메이트 신규 모집 시작 02"
        choice_book(driver, wait, challenge_name_value, book_name_value)
        challenge_detail(driver,wait, challenge_detail_value)
        start_index, end_index = 0, 0
        Recruitment_period(driver, wait, dates_list, start_index, end_index, 1, 1)
        start_index, end_index = 1, 1
        challenge_period(driver, wait, dates_list, start_index, end_index, 1, 1)
        mate_name_value = "서하" # 메이트명 검색
        search_mate(driver, wait, mate_name_value, "서하 통합 계정")  # 선택할 메이트 닉네임
        challenge_save(driver,wait)
        print("챌린지 신규 등록 성공")
    except Exception as e:
        logging.error(f"챌린지 신규 등록 테스트 중 오류가 발생했습니다: {str(e)}")
        return

    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()