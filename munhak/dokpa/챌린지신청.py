import logging, pyautogui
# setup
from munhak.module.setup_common_functions import (setup_driver, get_current_dir, get_parent_dir)
# admin
from munhak.module.admin_common_functions import (
    admin_login, choice_book, challenge_detail, Recruitment_period, challenge_period, search_mate, challenge_save,
    generate_date_range, challenge_tab, challenge_register)
# homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login)
# dokpa
from munhak.module.dokpa_common_functions import (
    dokpa_enter, all_challenge_apply, challenge_list)

# log
logger = logging.getLogger()
# path
current_dir = get_current_dir()
parent_dir = get_parent_dir(2)

def main():
    driver, wait = setup_driver()

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

    # 관리자 로그인
    admin_login(driver, admin_id, admin_pw)

    # 관리자 챌린지 탭 진입
    challenge_tab(driver,wait)

    # 관리자 챌린지탭 > 등록 선택
    challenge_register(driver, wait)

    # 도서 선택 & 챌린지 명 입력
    book_name_value = "해리" # 도서명 검색
    challenge_name_value = "서하 자동화 테스트 - 신청 직후 01" # 챌린지명 입력
    choice_book(driver, wait, challenge_name_value, book_name_value)

    # 챌린지 상세설명 입력
    challenge_detail_value = "서하 자동화 테스트 상세 설명" # 챌린지 상세설명 입력
    challenge_detail(driver, wait, challenge_detail_value)

    # 모집기간 설정
    start_index, end_index = 0, 0
    Recruitment_period(driver, wait, dates_list, start_index, end_index, 1, 1)

    # 챌린지 기간 설정
    start_index, end_index = 3, 3
    challenge_period(driver, wait, dates_list, start_index, end_index, 1, 1)

    # 메이트 설정
    mate_name_value = "서하" # 메이트명 검색
    search_mate(driver, wait, mate_name_value, "서하 통합 계정")  # 선택할 메이트 닉네임

    # 관리자 > 챌린지 저장
    challenge_save(driver, wait)

    # 문학동네 홈페이지 진입
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    home_page(driver, wait)

    # 문학동네 로그인
    munhak_login(driver, wait, user_id, user_pw)

    # 독파 진입 및 팝업 닫기 함수
    dokpa_enter(driver, wait)
    driver.switch_to.window(driver.window_handles[2])

    # 전체 챌린지 탭 진입
    all_challenge_apply(driver, wait)

    # 전체 > 신청완료X && 모집중 챌린지 신청까지
    challenge_list(driver, wait)

    # test_exit
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()
