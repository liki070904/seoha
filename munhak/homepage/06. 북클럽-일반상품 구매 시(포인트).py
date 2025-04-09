import logging, pyautogui
# setup
from munhak.module.setup_common_functions import (setup_driver, get_current_dir, get_parent_dir)
# homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, munhak_mypage, bookclub_click, shop_click, product_click, buy_product, bookclub_point_payment, bookclub_payment_click, my_sub_list)

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
    # 북클럽 진입
    bookclub_click(driver)
    driver.switch_to.window(driver.window_handles[-1])
    # SHOP 진입
    shop_click(driver)
    # 상품 선택
    product_click(driver,wait)
    # 구매하기 선택
    buy_product(driver)
    # 결제(포인트) 선택
    bookclub_point_payment(driver)
    # 결제하기 선택
    bookclub_payment_click(driver)
    # 마이페이지 진입
    munhak_mypage(driver)
    # 마이페이지 > 정기구독 내역 진입
    my_sub_list(driver)


    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()