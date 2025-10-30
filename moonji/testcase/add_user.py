import logging, pyautogui, time

from n2common.web.setup_module import (setup_driver, fill_form_field, navigation, switch_iframe, save_data)
from module.manager_common_functions import (manager_open, handle_popup_confirm)
from module.homepage_common_functions import intro_skip

logger = logging.getLogger()

def main():
    driver, wait = setup_driver()
    try:
        # ✅ 회원정보 변수
        user_id = "seoha63"
        user_pw = "admin135!"
        user_email = "seoha.lee63@ntoday.kr"
        user_name = "이서하"
        user_phone = "01026262626"

        # 관리자 로그인
        manager_open(driver, wait, "https://dev-moonji-mng.ntoday.kr")
        fill_form_field(driver, wait, "userId", "admin0", field_type="text", ui_name="ID 입력")
        fill_form_field(driver, wait, "userPw", "admin123$%^", field_type="text", ui_name="PW 입력")
        fill_form_field(driver, wait, "//button[contains(@class, 'fill_primary btn_login')]", None, field_type="click", ui_name="로그인 버튼")

        # 회원관리 > 회원등록
        navigation(driver, wait, "회원관리", "회원관리")
        switch_iframe(driver, "toBeAdmin")
        fill_form_field(driver, wait, "//a[contains(@class, 'fill_grey70')]", None, field_type="click", ui_name="등록 버튼")
        fill_form_field(driver, wait, "userId", user_id, field_type="text", ui_name="회원 등록 ID 입력")
        fill_form_field(driver, wait, "email", user_email, field_type="text", ui_name="회원 등록 이메일 입력")
        fill_form_field(driver, wait, "userPwd", user_pw, field_type="text", ui_name="회원 등록 PW 입력")
        fill_form_field(driver, wait, "userPwdConfirm", user_pw, field_type="text", ui_name="회원 등록 PW 확인 입력")
        fill_form_field(driver, wait, "userNm", user_name, field_type="text", ui_name="회원 등록 이름 입력")
        fill_form_field(driver, wait, "ctpn", user_phone, field_type="text", ui_name="회원 등록 휴대폰 입력")
        time.sleep(2)
        save_data(driver)
        handle_popup_confirm(driver, wait)

        # 새창 열기
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        # 문지 페이지 진입
        driver.get("https://dev-moonji.ntoday.kr")
        intro_skip(driver, wait)

        # 로그인
        fill_form_field(driver, wait, "//a[contains(text(), '로그인')]", None, field_type="click", ui_name="GNB-로그인 버튼")
        fill_form_field(driver, wait, "userId", user_id, field_type="text", ui_name="ID 입력")
        fill_form_field(driver, wait, "userPw", user_pw, field_type="text", ui_name="PW 입력")
        fill_form_field(driver, wait, "//button[contains(@class, 'fill_black')]", None, field_type="click", ui_name="로그인 버튼")

        # ✅ 테스트 완료 알림
        pyautogui.confirm(
            title='✅ Complete',
            text='문지 관리자 회원 등록 > 정상 로그인 완료'
        )

    except Exception as e:
        logger.exception(f"테스트 중 오류 발생 : {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


