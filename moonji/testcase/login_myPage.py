import logging, pyautogui

from n2common.web.setup_module import (setup_driver, fill_form_field)
from module.homepage_common_functions import (homepage_open, intro_skip)

logger = logging.getLogger()

def main():
    driver, wait = setup_driver()
    try:
        # ✅ FSS 관리자 로그인
        driver.get("https://dev-moonji.ntoday.kr")
        intro_skip(driver, wait)
        fill_form_field(driver, wait, "//a[contains(text(), '로그인')]", None, field_type="click")
        fill_form_field(driver, wait, "userId", "seoha30", field_type="text")
        fill_form_field(driver, wait, "userPw", "admin135!", field_type="text")
        fill_form_field(driver, wait, "//button[contains(@class, 'fill_black')]", None, field_type="click")
        logger.info("✅ 로그인 완료")
        fill_form_field(driver, wait, "//a[contains(text(), '마이페이지')]", None, field_type="click")
        logger.info("✅ 마이페이지 진입")

        # ✅ 테스트 완료 알림
        pyautogui.confirm(
            title='✅ Complete',
            text='테스트 완료'
        )

    except Exception as e:
        logger.exception(f"테스트 중 오류 발생 : {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

