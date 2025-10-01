import logging, pyautogui, time
# setup
from n2common.web.setup_module import (setup_driver, get_current_dir, get_parent_dir)
# manager
from module.manager_common_functions import (
    manager_login, channel_reserve_management, click_channel_option, click_search_reserve_detail,
    check_reservation_status)
# wel
from module.homepage_common_functions import (
    otour_homepage_open, otour_login, travel_products_package, select_supplier, select_product, fill_reservation_form, input_traveler_info,
    complete_reservation, check_reservation, navigate_to_reservation_list, process_payment, complete_payment, click_my_travel)
# log
logger = logging.getLogger()
# path
current_dir = get_current_dir()
parent_dir = get_parent_dir(2)

# 복지몰 홈페이지 입력
# ID 입력  개발:otourtest / 운영:sbrr103   /   포스코이앤씨 : seoha
# 비밀번호 입력  개발 : cjmall2$ / 운영 : cj011992???

def main():
    driver, wait = setup_driver()

    # 복지몰 URL
    otour_homepage_open(driver, wait)
    # 로그인
    otour_login(driver, wait, "otourtest", "cjmall2$")
    # 패키지 선택
    travel_products_package(driver, wait, "해외패키지", "동남아/대만/서남아", "방콕/파타야")
    # 공급사 태그 클릭 -> 한진 : HJ / 롯데 : LO / 하나 : HN / 모두 : MO
    select_supplier(driver, wait, "LO")
    # 상품 선택
    select_product(driver, wait)
    # 예약하기 버튼 클릭
    fill_reservation_form(driver, wait)
    # 여행자 정보 입력
    input_traveler_info(driver, wait, "테스트", "19880728", "seoha.lee@ntoday.kr","01022077353", "LEE", "SEOHA")
    # 예약 버튼 클릭
    complete_reservation(driver, wait)
    # 예약내역 확인 클릭
    check_reservation(driver, wait)
    # 예약 리스트 바로가기 클릭
    navigate_to_reservation_list(driver, wait)
    # 관리자 새탭 열기
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    # 관리자 로그인
    manager_login(driver, wait, "wlocos", "hanabiz!@#", "오투어")
    # 예약조회 진입
    channel_reserve_management(driver, wait)
    # 채널 선택  (오투어 : channelSeqArr1 / 복지몰 : channelSeqArr2 / 삼성전기 : channelSeqArr10)
    click_channel_option(driver, wait, "channelSeqArr2")
    # 예약 상세 진입
    click_search_reserve_detail(driver, wait)
    # 예약 확정 선택
    check_reservation_status(driver, wait)
    # 이전 탭으로 전환
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.5)
    # 페이지 새로고침
    driver.refresh()
    time.sleep(2)
    # 결제하기 선택
    process_payment(driver, wait)
    # 포인트 결제
    complete_payment(driver, wait)
    # 마이페이지 이동
    click_my_travel(driver, wait)

    # test_exit
    pyautogui.confirm(title = 'complete', text = '테스트 완료')

if __name__ == "__main__":
    main()

