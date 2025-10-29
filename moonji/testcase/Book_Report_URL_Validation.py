import logging, pyautogui

from n2common.web.setup_module import (setup_driver, fill_form_field)
from n2common.web.verify_module import (verify_url)
from module.homepage_common_functions import (intro_skip, navigation_moonji)

logger = logging.getLogger()

def main():
    driver, wait = setup_driver()
    try:
        # ✅ FSS 관리자 로그인
        driver.get("https://dev-moonji.ntoday.kr")
        intro_skip(driver, wait)
        navigation_moonji(driver, wait, "도서/저자", "자료실")
        fill_form_field(driver, wait, "//button[@data-key='category' and @data-value='32']", None, field_type="click", ui_name="독후활동지 버튼")
        verify_url(driver, "https://dev-moonji.ntoday.kr/bookAndAuthor/dataroom/list?page=1&type=32", exact=True)

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

