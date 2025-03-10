import logging, os, pyautogui, sys, time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # setup
from munhak.module.setup_common_functions import (setup_driver)
    # homepage
from munhak.module.homepage_common_functions import (
    home_page, munhak_login, munhak_mypage, mydata_change, withdraw, withdraw_confirm)

def main():
    driver, wait = setup_driver()

    # 문학동네 홈페이지 진입
    home_page(driver, wait)
    # 로그인
    time.sleep(1)
    munhak_login(driver, wait, "seoha50@ntoday.kr", "admin123")
    # 마이페이지 진입
    munhak_mypage(driver, wait)
    # 회원정보 변경 진입
    mydata_change(driver, wait, "admin123")
    # 회원 탈퇴 버튼 선택
    withdraw(driver, wait)
    # 회원탈퇴
    withdraw_confirm(driver,wait)

    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()