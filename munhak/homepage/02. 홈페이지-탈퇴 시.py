import logging, pyautogui
# setup
from munhak.module.setup_common_functions import (setup_driver, get_current_dir, get_parent_dir)
    # homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, munhak_mypage, mydata_change, withdraw, withdraw_confirm)

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
    munhak_login(driver, wait, "seoha50@ntoday.kr", "admin123")
    # 마이페이지 진입
    munhak_mypage(driver)
    # 회원정보 변경 진입
    mydata_change(driver, "admin123")
    # 회원 탈퇴 버튼 선택
    withdraw(driver)
    # 회원탈퇴
    withdraw_confirm(driver)

    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()