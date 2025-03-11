import logging, pyautogui
# setup
from munhak.module.setup_common_functions import (setup_driver, get_current_dir, get_parent_dir)
# homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, munhak_mypage, quarterly_click, sub_date_set, sub_init_set, giveaway_book, payment_agree, payment_click, my_sub_list)

# log
logger = logging.getLogger()
# path
current_dir = get_current_dir()
parent_dir = get_parent_dir(2)

def main():
    driver, wait = setup_driver()

    # 문학동네 홈페이지 진입
    home_page(driver, wait)
    # 로그인
    munhak_login(driver, wait, "seoha40@ntoday.kr", "admin123")
    # 계간 문학동네 진입
    quarterly_click(driver)
    # 정기구독 기간 설정  // 1년 = period1_01, 2년 = period1_02, 3년 = period1_03
    sub_date_set(driver, wait, "period1_02")
    # 정기구독 개시 설정  // 봄 , 여름 , 가을 , 겨울
    sub_init_set(driver, "여름")
    # 증정도서 선택
    giveaway_book(driver)
    # 결제(포인트) 선택
    payment_agree(driver)
    # 결제하기 선택
    payment_click(driver)
    # 마이페이지 진입
    munhak_mypage(driver)
    # 마이페이지 > 정기구독 내역 진입
    my_sub_list(driver)


    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()