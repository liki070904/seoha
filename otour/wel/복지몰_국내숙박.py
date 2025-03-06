import logging, os, pyautogui, sys, time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# setup
from otour.module.setup_common_functions import (setup_driver)
# manager
from otour.module.manager_common_functions import (
    some_function, manager_open, manager_login, channel_reserve_management, click_channel_option, click_search_reserve_detail,
    scroll_to_bottom, payment_info)
# wel
from otour.module.wel_common_functions import (
    homepage_open, login, travel_products_domestic, low_price, click_product, change_date, immediate_payment, reservation_info,
    add_twin_option,
    agree_conditions, complete_reservation, check_reservation, navigate_to_reservation_list, process_payment,
    complete_payment, click_my_travel, point_pay, click_payment)
# log
logger = logging.getLogger()

def main():
    driver, wait = setup_driver()
    some_function()

    # 복지몰 홈페이지 입력
    # driver.get("https://wel.hanabizwel.com/")   #운영
    # ID 입력  개발:otourtest, seohaqa / 운영:sbrr103   /   포스코이앤씨 : seoha
    # 비밀번호 입력  개발 : cjmall2$, rhaoddl1143! / 운영 : cj011992???

    # 복지몰 URL
    homepage_open(driver, wait)
    # 로그인
    login(driver, wait, "seohaqa", "rhaoddl1143!")
    # 국내숙박 선택
    travel_products_domestic(driver, wait)
    # 낮은 가격순 필터 선택
    low_price(driver, wait)
    # 국내숙박 결제용 상품 선택
    click_product(driver, wait)
    driver.switch_to.window(driver.window_handles[1])
    # 날짜 변경
    change_date(driver, wait)
    # 즉시결제 선택
    immediate_payment(driver, wait)
    # 예약자 정보 입력
    reservation_info(driver, wait, "테스트", "19880728", "seoha.lee@ntoday.kr","01022077353")
    driver.execute_script("window.scrollBy(0, 800);")
    # 트윈 옵션, 메모 추가
    add_twin_option(driver, wait, "테스트 예약 입니다.")
    # 약관 동의
    agree_conditions(driver, wait)
    scroll_to_bottom(driver)
    # 포인트 사용
    point_pay(driver, wait)
    # 결제하기
    click_payment(driver,wait)
    # 예약내역 확인 클릭
    check_reservation(driver, wait)
    # 예약 리스트 바로가기 클릭
    navigate_to_reservation_list(driver, wait)
    # 관리자 새탭 열기
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    manager_open(driver, wait)
    # 관리자 로그인
    manager_login(driver, wait, "wlocos", "hanabiz!@#", "2")
    # 예약조회 진입
    channel_reserve_management(driver, wait)
    # 채널 선택  (오투어 : channelSeqArr1 / 복지몰 : channelSeqArr2 / 삼성전기 : channelSeqArr10)
    click_channel_option(driver, wait, "channelSeqArr2")
    # 예약 상세 진입
    click_search_reserve_detail(driver, wait)
    # 결제정보 탭 진입
    payment_info(driver, wait)
    # test_exit
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()

