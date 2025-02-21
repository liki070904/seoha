import time, logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta

# iframe
def iframe(driver, wait):
    iframe = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[3]/div/iframe')
    driver.switch_to.frame(iframe)
# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
def some_function():
    logging.info("some_function 호출됨")
# 클릭
def click(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, 5, 5)  # 버튼의 (5, 5) 위치로 이동
    actions.click().perform()
# 요소가 보이는 영역 안에 있도록 스크롤하는 함수
def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
# 팝업 닫기 함수
def close_popup(driver, wait, popup_id, close_button_locator):
    try:
        popup_exists = driver.execute_script(f"return document.getElementById('{popup_id}') !== null;")
        if popup_exists:
            close_button = wait.until(EC.presence_of_element_located(close_button_locator))
            scroll_into_view(driver, close_button)
            click(driver, close_button)
            print("팝업 닫기 완료")
        else:
            print("팝업이 존재하지 않습니다.")
    except Exception as e:
        print(f"팝업 닫기 중 오류 발생: {e}")
    time.sleep(2)
# 관리자 로그인
def admin_login(driver, admin_homepage_url, admin_id, admin_pw):
    try:
        driver.get(admin_homepage_url)
        driver.find_element(By.ID, "userId").send_keys(admin_id)
        driver.find_element(By.ID, "userPw").send_keys(admin_pw)
        time.sleep(1)
        login_button = driver.find_element(By.CLASS_NAME, "btn_login")
        click(driver, login_button)
        logger.info("관리자 로그인 성공")
        time.sleep(2)
    except Exception as e:
        logging.error(f"관리자 로그인 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 챌린지 탭 진입
def challenge_tab(driver, wait):
    try:
        dokpa_management = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[5]/a")
        click(driver, dokpa_management)
        time.sleep(0.5)
        challenge_management = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[5]/ul/li[2]/a")
        click(driver, challenge_management)
        time.sleep(0.5)
        challenge_click = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[5]/ul/li[2]/ul/li[1]/a")
        click(driver, challenge_click)
        time.sleep(1)
        logger.info("챌린지 탭 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 탭 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 챌린지탭 > 등록 선택
def challenge_register(driver, wait):
    try:
        iframe(driver, wait)
        challenge_register = driver.find_element(By.XPATH, "//*[@id='searchForm']/div[2]/div[2]/a")
        click(driver, challenge_register)
        time.sleep(1)
        logger.info("챌린지 탭 등록 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"챌린지 탭 등록 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 시크릿 선택
def secret_radio(driver, wait, nondscsPwd):
    try:
        secret_radio = driver.find_element(By.XPATH, "//*[@id='munhakWrap']/table/tbody/tr[1]/td[1]/div/div[2]/label")
        click(driver, secret_radio)
        driver.find_element(By.ID, "nondscsPwd").send_keys(nondscsPwd)
        logger.info("시크릿 라디오, 비번 입력 성공")
        return nondscsPwd
    except Exception as e:
        logging.error(f"시크릿 라디오, 비번 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 도서 선택 & 챌린지 명 입력
def choice_book(driver, wait, challenge_name_value, book_name_value):
    try:
        # 도서 선택
        book_choice_popup = driver.find_element(By.XPATH, "//*[@id='munhakWrap']/table/tbody/tr[2]/td/div/button")
        click(driver, book_choice_popup)
        time.sleep(2)
        # 도서명 입력
        book_name = driver.find_element(By.XPATH, "//*[@id='srchBookLyrSearchWord']")
        book_name.clear()
        book_name.send_keys(book_name_value)
        time.sleep(1)
        # 검색 버튼 클릭
        search_button = driver.find_element(By.XPATH, "//*[@id='srchBookPop']/div[2]/div[2]/div[1]/div[2]/button[1]")
        click(driver, search_button)
        time.sleep(1)
        # 첫번째 도서 선택
        WebDriverWait(driver, 30).until_not(
            EC.text_to_be_present_in_element((By.XPATH, "//*[@id='bookTbody']/tr[1]"), "조회 중입니다. 잠시만 기다려주세요.")
        )
        click_first_book = driver.find_element(By.XPATH, "//*[@id='bookTbody']/tr[1]")
        click(driver, click_first_book)
        # 도서 선택 완료 버튼 클릭
        book_choice_complete = driver.find_element(By.XPATH, "//*[@id='srchBookPop']/div[2]/div[3]/button")
        click(driver, book_choice_complete)
        time.sleep(1)
        # 챌린지명 입력
        challenge_name = driver.find_element(By.XPATH, "//*[@id='chlngNm']")
        challenge_name.clear()
        challenge_name.send_keys(challenge_name_value)
        time.sleep(0.5)
        logger.info("도서 선택 & 챌린지 명 입력 성공")
        return challenge_name_value, book_name_value
    except Exception as e:
        logging.error(f"도서 선택 & 챌린지 명 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 챌린지 상세설명 입력
def challenge_detail(driver, wait, challenge_detail_value):
    try:
        challenge_detail = driver.find_element(By.XPATH, '//*[@id="cke_1_contents"]/iframe')
        driver.switch_to.frame(challenge_detail)
        challenge_detail = driver.find_element(By.XPATH, '//body')
        challenge_detail.send_keys(challenge_detail_value)
        driver.switch_to.default_content()
        time.sleep(1)
        logger.info("챌린지 상세 입력 성공")
        return challenge_detail_value
    except Exception as e:
        logging.error(f"챌린지 상세 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 메이트 설정
def search_mate(driver, wait, mate_name_value, account_name):
    try:
        search_mate = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/table/tbody/tr[11]/td[2]/div/div/button')
        driver.execute_script("arguments[0].scrollIntoView(true);", search_mate)
        click(driver, search_mate)
        mate_name = driver.find_element(By.XPATH, '//*[@id="mateLyrSearchWord"]')
        mate_name.send_keys(mate_name_value)
        search = driver.find_element(By.XPATH, '//*[@id="searchMatePop"]/div[2]/div[2]/div[1]/div[2]/button[1]')
        click(driver, search)
        time.sleep(2)
        table = driver.find_element(By.XPATH, '//*[@id="mateLyrTbody"]')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) > 1:
                if cells[1].text.strip() == account_name:
                    # 해당 행 클릭
                    click(driver, row)
                    break
        logger.info("메이트 설정 성공")
        return mate_name_value
    except Exception as e:
        logging.error(f"메이트 설정 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지 저장
def challenge_save(driver, wait):
    try:
        time.sleep(2)
        challenge_save = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/button')
        click(driver, challenge_save)
        time.sleep(1)
        pop_up1 = driver.find_element(By.XPATH, '//*[@id="saveAlert"]/div[2]/div[2]/a[2]')
        click(driver, pop_up1)
        time.sleep(1)
        pop_up2 = driver.find_element(By.XPATH, '//*[@id="alert"]/div[2]/div[2]/a')
        click(driver, pop_up2)
        time.sleep(3)
        logger.info("챌린지 저장 성공")
    except Exception as e:
        logging.error(f"챌린지 저장 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지 수정
def challenge_edit(driver, wait):
    try:
        time.sleep(1)
        challenge_edit= driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/button')
        click(driver, challenge_edit)
        pop_up1 = driver.find_element(By.XPATH, '//*[@id="saveAlert"]/div[2]/div[2]/a[2]')
        click(driver, pop_up1)
        time.sleep(1)
        logger.info("챌린지 수정 성공")
    except Exception as e:
        logging.error(f"챌린지 저장 완료 테스트 중 오류가 발생 했습니다: {str(e)}")
        return
# 관리자 챌린지 재진입
def choice_challenge(driver, wait):
    try:
        iframe(driver, wait)
        choice_challenge = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/table/tbody/tr[1]/td[4]/a')
        click(driver, choice_challenge)
        time.sleep(3)
        logger.info("챌린지 재진입 성공")
    except Exception as e:
        logging.error(f"챌린지 재진입 테스트 중 오류가 발생 했습니다: {str(e)}")
        return
# 날짜 지정 min_days : 0 -> today, min_days : -1 -> yesterday 시작일(start_date), 종료일(end_date), 날짜 배열(dates_list)
def generate_date_range(min_days=0, max_days=3):
    # 시작일자 계산
    start_date = (datetime.now() - timedelta(days=min_days)).day
    # 최대 날짜까지 날짜 리스트 생성
    dates_list = [(datetime.now() + timedelta(days=i)).day for i in range(min_days, max_days + 1)]
    # 결과 반환
    return {
        'start_date': start_date,
        'end_date': dates_list[-1],
        'dates_list': dates_list,
    }
# 모집기간 설정
def Recruitment_period(driver, wait, dates_list, start_index, end_index, desired_start_month, desired_end_month):
    try:
        #모집기간 설정
        iframe(driver, wait)
        recruitment_calendar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'rcritDtStr')))
        driver.execute_script("arguments[0].scrollIntoView(true);", recruitment_calendar)
        click(driver, recruitment_calendar)
        desired_start_date  = str(dates_list[start_index])  #모집시작날짜 선택
        desired_end_date  = str(dates_list[start_index])    #모집종료날짜 선택
        month_classes = ["ui-datepicker-group-first", "ui-datepicker-group-last"]
        start_month_class = month_classes[desired_start_month - 1]
        end_month_class = month_classes[desired_end_month - 1]
        # 시작일자 캘린더
        start_month_picker = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='ui-datepicker-div']/div[contains(@class, '{start_month_class}')]")))
        startDate = start_month_picker.find_element(By.XPATH, f".//td/a[text()='{desired_start_date}']")
        if startDate.text == desired_start_date:
            click(driver, startDate)
        time.sleep(1)
        # 종료일자 캘린더
        end_month_picker = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='ui-datepicker-div']/div[contains(@class, '{end_month_class}')]")))
        endDate = end_month_picker.find_element(By.XPATH, f".//td/a[text()='{desired_end_date}']")
        if endDate.text == desired_end_date:
            click(driver, endDate)
        time.sleep(1)
        logger.info("모집 기간 설정 성공")
    except Exception as e:
        logging.error(f"모집 기간 설정 완료 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 챌린지 기간 설정
def challenge_period(driver, wait, dates_list, start_index, end_index , challenge_start_month, challenge_end_month):
    try:
        # 챌린지 기간 설정
        challenge_calendar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'chlngDtStr')))
        driver.execute_script("arguments[0].scrollIntoView(true);", challenge_calendar)
        click(driver, challenge_calendar)
        challenge_start_date  = str(dates_list[start_index])  #챌린지시작날짜 선택
        challenge_end_date  = str(dates_list[end_index])    #챌린지종료날짜 선택
        month_classes = ["ui-datepicker-group-first", "ui-datepicker-group-last"]
        start_month_class = month_classes[challenge_start_month - 1]
        end_month_class = month_classes[challenge_end_month - 1]
        # 시작일자 캘린더
        start_month_picker = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='ui-datepicker-div']/div[contains(@class, '{start_month_class}')]")))
        startDate = start_month_picker.find_element(By.XPATH, f".//td/a[text()='{challenge_start_date}']")
        if startDate.text == challenge_start_date:
            click(driver, startDate)
        time.sleep(1)
        # 종료일자 캘린더
        end_month_picker = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='ui-datepicker-div']/div[contains(@class, '{end_month_class}')]")))
        endDate = end_month_picker.find_element(By.XPATH, f".//td/a[text()='{challenge_end_date}']")
        if endDate.text == challenge_end_date:
            click(driver, endDate)
        time.sleep(1)
        logger.info("챌린지 기간 설정 성공")
    except Exception as e:
        logging.error(f"챌린지 기간 설정 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지 탭 닫기
def close_challenge(driver, wait):
    try:
        driver.switch_to.default_content()
        close_challenge = driver.find_element(By.XPATH, '//*[@id="myTabbar"]/div/div/div[1]/div[2]/div/div[3]/div[2]')
        click(driver, close_challenge)
        logger.info("챌린지 탭 닫기 성공")
    except Exception as e:
        logging.error(f"챌린지 탭 닫기 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지현황 진입
def challenge_status(driver, wait):
    try:
        challenge_click = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[5]/ul/li[2]/ul/li[3]/a")
        click(driver, challenge_click)
        time.sleep(2)
        logger.info("챌린지 현황 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 현황 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지현황 > 전체보기
def all_challenge_status(driver, wait):
    try:
        driver.switch_to.default_content()
        iframe(driver, wait)
        time.sleep(2)
        # 갯수보기 선택
        nice_select = driver.find_element(By.XPATH, '//*[@id="searchForm"]/div[2]/div/div[2]')
        click(driver, nice_select)
        time.sleep(1)
        # 전체 보기 선택
        all_select = driver.find_element(By.XPATH, '//*[@id="searchForm"]/div[2]/div/div[2]/div/ul/li[6]')
        click(driver, all_select)
        time.sleep(2)
        logger.info("챌린지 현황 > 전체보기 성공")
    except Exception as e:
        logging.error(f"챌린지 현황 > 전체보기 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지현황 > 챌린지
def select_challenge(driver, wait, challenge_name_value):
    try:
        length = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/table/tbody/tr[1]/td[1]')
        value = int(length.text)
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(value):
            rows = driver.find_elements(By.XPATH, '//*[@id="munhakWrap"]/div[2]/table/tbody/tr')
            challenege_found = False
            for row in rows:
                cell = row.find_elements(By.TAG_NAME, "td")[1]
                link = cell.find_element(By.CSS_SELECTOR, 'a')
                if link.text == challenge_name_value:
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(1)
                    click(driver, link)
                    print("챌린지 현황 > 챌린지 클릭 성공")
                    challenege_found = True
                    time.sleep(3)
                    break
            if challenege_found:
                return True
            else:
                print("챌린지 클릭 실패, 스크롤 내림")
                driver.execute_script("window.scrollTo(0, 1000);")
                time.sleep(0.5)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("더 이상 스크롤 할 수 없습니다.")
                    break
                last_height = new_height
        time.sleep(3)
        logger.info("챌린지 현황 > 챌린지 진입 성공")
        return False
    except Exception as e:
        logging.error(f"챌린지 현황 > 챌린지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 미션 추가
def add_mission(driver, wait, mission_name_value, mission_answer_value):
    try:
        # 미션 등록 버튼
        btn_mission = driver.find_element(By.XPATH,'//*[@id="munhakWrap"]/div[2]/div[2]/div/div[1]/div[2]/button')
        click(driver, btn_mission)
        time.sleep(1)
        # 미션명 입력
        mission_name = driver.find_element(By.XPATH,'//*[@id="missionNm"]')
        mission_name.clear()
        mission_name.send_keys(mission_name_value)
        time.sleep(1)
        # 미션 캘린더 선택
        mission_date = driver.find_element(By.XPATH,'//*[@id="missionRegisterPop"]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[1]/div')
        click(driver, mission_date)
        time.sleep(1)
        # 미션시작일자 선택
        mission_start_date = driver.find_element(By.CSS_SELECTOR, '[class$="today"]')
        click(driver, mission_start_date)
        time.sleep(1)
        # 미션 답변 입력
        mission_answer = driver.find_element(By.XPATH,'//*[@id="aswItem1"]')
        mission_answer.clear()
        mission_answer.send_keys(mission_answer_value)
        time.sleep(1)
        # 미션 저장
        mission_save = driver.find_element(By.XPATH,'//*[@id="missionRegisterPop"]/div[2]/div[3]/button[2]')
        click(driver, mission_save)
        # 미션 저장 > 확인
        click_confirm = driver.find_element(By.XPATH, '//*[@id="missionSaveBtn"]')
        click(driver, click_confirm)
        logger.info("미션 추가 성공")
        return mission_name_value, mission_answer_value
    except Exception as e:
        logging.error(f"미션 추가 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 챌린지 > 최상위 챌린지 진입
def top_challenge(driver, wait):
    try:
        iframe(driver, wait)
        choice_challenge = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/table/tbody/tr[1]/td[4]/a')
        click(driver,choice_challenge)
        time.sleep(1)
        logger.info("최상위 챌린지 진입 성공")
    except Exception as e:
        logging.error(f"최상위 챌린지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 챌린지현황 > 공지사항 등록
def add_announcement(driver, wait, announcement_name_value, announcement_particular_value):
    try:
        time.sleep(2)
        # 공지사항 탭 진입
        announcement_click = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/div[1]/ul/li[2]/a')
        click(driver, announcement_click)
        print("공지사항 탭 진입 성공")
        time.sleep(2)
        # 공지사항 추가 선택
        btn_announcement = driver.find_element(By.XPATH,'//*[@id="searchForm"]/div[2]/div[2]/a')
        click(driver,btn_announcement)
        print("공지사항 추가 클릭 성공")
        time.sleep(1)
        # 공지사항 타이틀 입력
        announcement_name = driver.find_element(By.XPATH, '//*[@id="ttl"]')
        announcement_name.clear()
        announcement_name.send_keys(announcement_name_value)
        print("공지사항 타이틀 입력 성공")
        time.sleep(1)
        # 공지사항 상세 iframe 전환
        announcement_particular = driver.find_element(By.XPATH, '//*[@id="cke_1_contents"]/iframe')
        driver.switch_to.frame(announcement_particular)
        print("공지사항 상세 iframe 전환 성공")
        # 공지사항 상세 입력
        announcement_particular = driver.find_element(By.XPATH,'//body')
        announcement_particular.clear()
        announcement_particular.send_keys(announcement_particular_value)
        driver.switch_to.default_content()
        print("공지사항 상세 입력 성공")
        time.sleep(1)
        # 저장 선택
        iframe(driver,wait)
        announcement_save = driver.find_element(By.XPATH,'//*[@id="munhakWrap"]/div[3]/button')
        click(driver, announcement_save)
        print("공지사항 저장 클릭 성공")
        time.sleep(1)
        # 확인 선택
        click_confirm = driver.find_element(By.XPATH, '//*[@id="saveAlert"]/div[2]/div[2]/a[2]')
        click(driver, click_confirm)
        print("공지사항 저장 확인 클릭 성공")
        logger.info("공지사항 추가 성공")
        return announcement_name_value, announcement_particular_value
    except Exception as e:
        logging.error(f"공지사항 추가 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 1:1관리 탭 진입
def site_management_tab(driver, wait):
    try:
        time.sleep(1)
        site_management_tab = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[3]/a")
        click(driver, site_management_tab)
        time.sleep(1)
        inquiry_management = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[3]/ul/li[6]/a")
        click(driver, inquiry_management)
        time.sleep(1)
        one_on_one = driver.find_element(By.XPATH, "//*[@id='aside']/div/nav/ul/li[3]/ul/li[6]/ul/li[1]/a")
        click(driver, one_on_one)
        time.sleep(2)
        logger.info("관리자 > 사이트 관리 진입 성공")
    except Exception as e:
        logging.error(f"관리자 > 사이트 관리 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 문의 선택
def inquiry_register(driver, wait, inquiry_title_value):
    try:
        inquiry_manage_title = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/table/tbody/tr[1]/td[3]/a/span')
        if inquiry_title_value == inquiry_manage_title.text:
            click(driver, inquiry_manage_title)
            time.sleep(1)
        logger.info("관리자 > 사이트관리 > 문의관리 진입 성공")
    except Exception as e:
        logging.error(f"관리자 > 사이트관리 > 문의관리 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 문의 답변
def answer_inquiry(driver, wait, answer_inquiry_value):
    try:
        #iframe진입
        answer_iframe = driver.find_element(By.XPATH, '//*[@id="cke_1_contents"]/iframe')
        driver.switch_to.frame(answer_iframe)
        time.sleep(1)
        answer_inquiry = driver.find_element(By.XPATH, '//body')
        answer_inquiry.send_keys(answer_inquiry_value)
        driver.switch_to.default_content()
        time.sleep(1)
        logger.info("문의 답변 입력 성공")
        return answer_inquiry_value
    except Exception as e:
        logging.error(f"문의 답변 입력 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 관리자 > 문의 > 답변여부 변경
def answerYN(driver, wait):
    try:
        driver.switch_to.default_content()
        iframe(driver, wait)
        answerYN = driver.find_element(By.XPATH,'//*[@id="form"]/table/tbody/tr[8]/td[1]/div/div/span')
        click(driver, answerYN)
        time.sleep(1)
        answerY = driver.find_element(By.XPATH, "//li[contains(text(), '답변완료')]")
        click(driver,answerY)
        time.sleep(1)
        logger.info("답변여부 : 답변완료 변경 성공")
    except Exception as e:
        logging.error(f"답변여부 : 답변완료 변경 테스트 중 오류가 발생했습니다: {str(e)}")
        return

# 관리자 > 문의 저장
def save_inquiry(driver, wait):
    try:
        save_inquiry = driver.find_element(By.XPATH, '//*[@id="munhakWrap"]/div[2]/button')
        click(driver, save_inquiry)
        time.sleep(0.5)
        click_confirm = driver.find_element(By.XPATH, '//*[@id="confirmBtn"]')
        click(driver, click_confirm)
        time.sleep(0.5)
        logger.info("문의 저장 성공")
    except Exception as e:
        logging.error(f"문의 저장 테스트 중 오류가 발생했습니다: {str(e)}")
        return

