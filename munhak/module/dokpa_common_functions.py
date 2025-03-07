import time, logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from munhak.module.setup_common_functions import (click, scroll_into_view, close_popup)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# 독파 진입 및 팝업 닫기 함수
def dokpa_enter(driver, wait):
    try:
        dokpa_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header']/div[1]/div/ul[1]/li[3]/a")))
        click(driver, dokpa_link)
        time.sleep(1)
        close_popup(driver, wait, 'popMainLayer', (By.ID, 'closePopupBtnToday'))
        time.sleep(2)
        logger.info("독파 진입 성공")
    except Exception as e:
        logging.error(f"독파 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 전체 챌린지 탭 진입
def all_challenge_apply(driver, wait):
    try:
        challenge_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[1]/ul/li[2]/a')))
        click(driver, challenge_link)
        time.sleep(1)
        logger.info("챌린지 전체 탭 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 전체 탭 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 커밍쑨 챌린지 탭 진입
def commingsoon_challenge_apply(driver, wait):
    try:
        challenge_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[1]/ul/li[5]/a')))
        click(driver, challenge_link)
        time.sleep(2)
        logger.info("커밍쑨 챌린지 탭 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 커밍쑨 탭 진입 테스트 중 오류가 발생 했습니다: {str(e)}")
        return
# 전체 > 신청완료X && 모집중 챌린지 진입
def same_challenge_name_value(driver, wait, challenge_name_value):
    try:
        challenge_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.challenge_list")))
        challenges = challenge_list.find_elements(By.TAG_NAME, "li")
        challenge_index = 1  # XPath 인덱스는 1부터 시작
        while challenge_index <= len(challenges):
            try:
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                challenge_element = driver.find_element(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]')
                challenge_click = challenge_element.find_element(By.CSS_SELECTOR, 'div > a')
                is_not_applied = not challenge_element.find_elements(By.XPATH, './/div[contains(@class, "badge app_complete")]')
                is_recruiting = challenge_element.find_elements(By.XPATH, './/p[contains(text(), "모집중")]')
                if is_not_applied and is_recruiting:
                    challenge_name_element = challenge_element.find_element(By.CSS_SELECTOR, 'div > strong.tit')
                    if challenge_name_element.text == challenge_name_value:
                        driver.execute_script("arguments[0].scrollIntoView(true);", challenge_click)
                        time.sleep(1)
                        click(driver, challenge_click)
                    break
                challenge_index +=1
                time.sleep(1)
            except TimeoutException:
                logging.error(f"{challenge_index}번째 챌린지 상세 진입 실패")
                time.sleep(1)
        logger.info("챌린지 진입 성공")
    except Exception as e:
        logging.error(f"챌린지 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 챌린지 필수동의
def challenge_apply_confirm(driver, wait):
    # 필수동의 체크
    required_agreement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="agreeChk"]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", required_agreement)
    click(driver, required_agreement)
    time.sleep(1)

    # '참여하기' 버튼 확인
    challenge_apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="joinBtn"]/span')))
    driver.execute_script("arguments[0].scrollIntoView(true);", challenge_apply_button)
    click(driver,challenge_apply_button)
    time.sleep(1)

    # 챌린지 신청 완료 팝업
    challenge_complete_popup = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.fill_black[onclick=\"layerHide('checkAlert')\"]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", challenge_complete_popup)
    click(driver,challenge_complete_popup)
    time.sleep(1)
# 전체 > 신청완료X && 모집중 챌린지 신청까지
def challenge_list(driver, wait):
    try:
        challenge_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.challenge_list")))
        challenges = challenge_list.find_elements(By.TAG_NAME, "li")
        challenge_index = 1  # XPath 인덱스는 1부터 시작
        while challenge_index <= len(challenges):
            try:
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                challenge_click = driver.find_element(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]/div/a')
                is_not_applied = not driver.find_elements(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]//div[contains(@class, "badge app_complete")]')
                is_recruiting = driver.find_elements(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]//p[contains(text(), "모집중")]')
                if is_not_applied and is_recruiting:
                    scroll_into_view(driver, challenge_click)
                    time.sleep(1)
                    click(driver, challenge_click)
                    logger.info("챌린지 진입 성공")
                    time.sleep(2)
                    challenge_apply_confirm(driver, wait)
                    time.sleep(1)
                    break
                elif is_not_applied and not is_recruiting:
                    print("신청가능한 챌린지가 없습니다.")
                    break
                else:
                    print(f"{challenge_index}번째 챌린지는 신청 완료 상태입니다.")
                    challenge_index += 1
                    time.sleep(1)
                    continue
            except TimeoutException:
                logging.error(f"{challenge_index}번째 챌린지 상세 진입 실패")
                time.sleep(1)
            challenge_index += 1  # 다음 챌린지로 이동
        logger.info("챌린지 신청 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"챌린지 신청 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 시크릿 챌린지 신청까지
def secret_challenge_list(driver, wait, challenge_name_value, secret_challenge_popup_value):
        try:
            challenge_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.challenge_list")))
            challenges = challenge_list.find_elements(By.TAG_NAME, "li")
            challenge_index = 1  # XPath 인덱스는 1부터 시작
            # found_challenge = False
            while challenge_index <= len(challenges):
                print(f"{challenge_index}번째 챌린지 진입 시작")
                try:
                    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    challenge_click = driver.find_element(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]/div/a')
                    # '신청 완료'가 없고 '모집중'인 경우
                    is_not_applied = not driver.find_elements(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]//div[contains(@class, "badge app_complete")]')
                    is_recruiting = driver.find_elements(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]//p[contains(text(), "모집중")]')
                    # class 속성에 'private'가 포함되어 있는지 확인
                    is_private_challenge = bool(driver.find_elements(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]//div[contains(@class, "private")]'))
                    # challenge_name_value와 같은 챌린지 이름인지 확인
                    challenge_name = driver.find_element(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]/div/a/div[2]/strong').text
                    if is_not_applied and is_recruiting and is_private_challenge and challenge_name == challenge_name_value:
                        # found_challenge = True
                        scroll_into_view(driver, challenge_click)
                        time.sleep(1)
                        click(driver,challenge_click)
                        time.sleep(2)
                        # 시크릿 챌린지 팝업 비밀번호 입력
                        print("시크릿 챌린지 팝업 비밀번호 입력 시작")
                        time.sleep(1)
                        try:
                            secret_challenge_popup = wait.until(EC.presence_of_element_located((By.ID, "nondscsPwd")))
                            secret_challenge_popup.clear()
                            secret_challenge_popup.send_keys(secret_challenge_popup_value)
                            secret_challenge_popup_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@onclick="fn_privateChallengeEntry()"]/span')))
                            click(driver, secret_challenge_popup_btn)
                            time.sleep(3)
                        except TimeoutException:
                            logging.error("시크릿 챌린지 팝업을 찾을 수 없습니다.")
                            return
                        time.sleep(3)
                        challenge_apply_confirm(driver, wait)
                        break
                    elif is_not_applied and not is_recruiting and not is_private_challenge:
                        print("신청가능한 챌린지가 없습니다.")
                        break
                    else:
                        print(f"{challenge_index}번째 챌린지는 신청 완료 상태입니다.")
                        challenge_index += 1
                        time.sleep(1)
                        continue
                except TimeoutException:
                    logging.error(f"{challenge_index}번째 챌린지 상세 진입 실패")
                    time.sleep(1)
                challenge_index += 1  # 다음 챌린지로 이동
            logger.info("시크릿 챌린지 신청 버튼 클릭 성공")
            return secret_challenge_popup_value
        except Exception as e:
            logging.error(f"챌린지 신청 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
            return
# 커밍쑨 신청 버튼 클릭
def comming_soon(driver, wait, challenge_name_value):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(3)
        challenge_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.challenge_list")))
        challenges = challenge_list.find_elements(By.TAG_NAME, "li")
        matching_challenges = []
        for challenge in challenges:
            challenge_name_element = challenge.find_element(By.CSS_SELECTOR, 'strong.tit')
            alert_button = challenge.find_element(By.XPATH, './/button[span[@class="txt_on"]]')
            if challenge_name_element.text == challenge_name_value and alert_button.text == '오픈 알림 받기':
                matching_challenges.append(challenge)
        if matching_challenges:
            if len(matching_challenges) >= 1:
                selected_challenge = matching_challenges[0]
            alert_button = selected_challenge.find_element(By.XPATH, './/button[span[@class="txt_on"]]')
            driver.execute_script("arguments[0].scrollIntoView(true);", alert_button)
            time.sleep(1)
            click(driver, alert_button)
            print('챌린지 오픈 알림 클릭')
            time.sleep(1)
        else:
            print('해당 텍스트를 찾을 수 없습니다.')
        logger.info("챌린지 신청 버튼 클릭 성공")
        time.sleep(1)
    except Exception as e:
        logging.error(f"챌린지 신청 버튼 클릭 테스트 중 오류가 발생 했습니다: {str(e)}")
        return
# 전체 > 신청완료X && 모집중 챌린지 찜하기 버튼 클릭
def challenge_apply_wishlist(driver, wait, challenge_name_value):
    try:
        challenge_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.challenge_list")))
        challenges = challenge_list.find_elements(By.TAG_NAME, "li")
        challenge_index = 1  # XPath 인덱스는 1부터 시작
        while challenge_index <= len(challenges):
            try:
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                challenge_element = driver.find_element(By.XPATH, f'//*[@id="challengeArea"]/li[{challenge_index}]')
                challenge_click = challenge_element.find_element(By.CSS_SELECTOR, 'div > a')
                is_not_applied = not challenge_element.find_elements(By.XPATH, './/div[contains(@class, "badge app_complete")]')
                is_recruiting = challenge_element.find_elements(By.XPATH, './/p[contains(text(), "모집중")]')
                if is_not_applied and is_recruiting:
                    challenge_name_element = challenge_element.find_element(By.CSS_SELECTOR, 'div > strong.tit')
                    if challenge_name_element.text == challenge_name_value:
                        driver.execute_script("arguments[0].scrollIntoView(true);", challenge_click)
                        time.sleep(1)
                        click(driver, challenge_click)
                        time.sleep(1)
                        # 챌린지 찜 선택
                        challenge_wishlist = driver.find_element(By.XPATH, '//*[@id="bookmarkBtn"]')
                        if 'active' in challenge_wishlist.get_attribute('class'):
                            print("찜하기 상태입니다.")
                            return
                        else:
                            click(driver, challenge_wishlist)
                            print("찜하기 선택했습니다.")
                        break
                challenge_index += 1
                time.sleep(1)
            except TimeoutException:
                logging.error(f"{challenge_index}번째 챌린지 상세 진입 실패")
                time.sleep(1)
        logger.info("챌린지 찜하기 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"챌린지 찜하기 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 메이트 찜하기
def myBookmark_mate(driver, wait):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)
        mate = driver.find_element(By.CSS_SELECTOR, '#mateNcnm')
        driver.execute_script("arguments[0].scrollIntoView(true);", mate)
        click(driver, mate)
        time.sleep(2)
        mate_bookmark_off_state = driver.find_element(By.CSS_SELECTOR, 'button.btn_like.myBookmarkBtn')
        if 'active' in mate_bookmark_off_state.get_attribute('class'):
            print("찜하기 상태입니다.")
            return
        else:
            click(driver, mate_bookmark_off_state)
            print("찜하기 선택했습니다.")
        time.sleep(2)
        logger.info("메이트 찜하기 버튼 클릭 성공")
    except Exception as e:
        logging.error(f"메이트 찜하기 버튼 클릭 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 마이독파 진입
def my_dokpa(driver, wait):
    try:
        time.sleep(2)
        my_dokpa = driver.find_element(By.XPATH, '//*[@id="footNav"]/div[3]/ul/li[5]/a')
        click(driver, my_dokpa)
        time.sleep(1)
        logger.info("마이독파 진입 성공")
    except Exception as e:
        logging.error(f"마이독파 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 마이독파 > 설정
def my_dokpa_setting(driver, wait):
    try:
        time.sleep(2)
        setting = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/a[2]')
        click(driver, setting)
        time.sleep(1)
        logger.info("마이독파 설정 진입 성공")
    except Exception as e:
        logging.error(f"마이독파 설정 진입 테스트 중 오류가 발생했습니다: {str(e)}")
        return
# 마이독파 > 1:1 문의
def my_dokpa_one_on_one(driver, wait, inquiry_title_value, inquiry_detail_value):
    try:
        # 1:1 문의 진입
        time.sleep(2)
        one_on_one = driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[2]/ul/li[3]/a')
        click(driver, one_on_one)
        time.sleep(1)
        # 문의하기 선택
        inquiry = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[1]/a/span')
        click(driver, inquiry)
        time.sleep(1)
        # 문의 타이틀 입력
        inquiry_title = driver.find_element(By.XPATH, '//*[@id="ttl"]')
        inquiry_title.clear()
        inquiry_title.send_keys(inquiry_title_value)
        time.sleep(1)
        # 문의 내용 입력
        inquiry_detail = driver.find_element(By.XPATH, '//*[@id="cn"]')
        inquiry_detail.clear()
        inquiry_detail.send_keys(inquiry_detail_value)
        time.sleep(1)
        # 문의 등록
        save_inquiry = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/button')
        click(driver, save_inquiry)
        time.sleep(1)
        save_inquiry_confirm = driver.find_element(By.XPATH, '//*[@id="confirmBtn"]')
        click(driver, save_inquiry_confirm)
        time.sleep(1)
        confirm = driver.find_element(By.XPATH, '//*[@id="alert"]/div[2]/div[2]/button')
        click(driver, confirm)
        time.sleep(1)
        logger.info("1:1문의 작성 성공")
        return inquiry_title_value, inquiry_detail_value
    except Exception as e:
        logging.error(f"1:1문의 작성 테스트 중 오류가 발생했습니다: {str(e)}")
        return

