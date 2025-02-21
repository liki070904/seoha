import logging, os, pyautogui, sys, time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    # setup
from munhak.module.setup_common_functions import (setup_driver)
    # homepage
from munhak.module.homepage_common_functions import (
    some_function, home_page, munhak_login, munhak_mypage, mydata_change, withdraw, withdraw_confirm)

def main():
    driver, wait = setup_driver()
    some_function()
    # 홈페이지 url, 계정
    homepage_url = "https://dev-munhak-home.ntoday.kr/"
    user_id = "seoha50@ntoday.kr"
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
        time.sleep(1)
        munhak_login(driver, wait, user_id, user_pw)
        print("로그인 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 마이페이지 진입
    try:
        munhak_mypage(driver, wait)
        print("마이페이지 진입 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"마이페이지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 회원정보 변경 진입
    try:
        mydata_change(driver, wait, user_pw)
        print("회원정보 변경 진입 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"회원정보 변경 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 회원 탈퇴 버튼 선택
    try:
        withdraw(driver, wait)
        print("회원 탈퇴 버튼 선택 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"회원 탈퇴 버튼 선택 테스트 중 오류가 발생했습니다: {str(e)}")
        return
    # 회원탈퇴
    try:
        withdraw_confirm(driver,wait)
        print("회원 탈퇴 성공")
    except Exception as e:
        logging.error(f"회원 탈퇴 테스트 중 오류가 발생했습니다: {str(e)}")
        return

    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()