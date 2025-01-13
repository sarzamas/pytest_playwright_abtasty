from os import linesep as ls

import pytest
from playwright.sync_api import expect


@pytest.mark.layout
def test_reset_psw_page_elements(page):
    """
    **Проверка элементов на странице восстановления пароля**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * переходим на страницу восстановления пароля
    * проверяем URL, title, заголовок, название страницы
    * проверяем наличие интерактивных элементов: полей ввода, кнопок и ссылок
    * проверяем наличие статических элементов верстки на странице

    Ожидаемый результат:

    * элементы отображаются в соответствии с требованиями дизайна
    """
    page, lang = page
    page.get_by_test_id('resetPasswordLink').click(position={'x': 10, 'y': 10})

    page.wait_for_url('**/reset-password')
    expect(page).to_have_url('https://auth.abtasty.com/reset-password')
    expect(page).to_have_title('AB Tasty - Experience Optimization Platform')
    expect(page.get_by_role("link", name="abtasty")).to_be_visible()
    expect(page.get_by_role('heading', name='Reset your password')).to_be_visible()

    expect(page.locator('#email')).to_be_visible()
    expect(page.get_by_role('button', name='Send me the password reset link')).to_be_visible()
    expect(page.get_by_role('link', name='Return to login')).to_be_visible()

    expect(page.get_by_text('Take a breath and enter the email address associated to your account. '
                            'We’ll send you an email with a link to reset your password.')).to_be_visible()
    expect(page.get_by_text('E-mail*')).to_be_visible()
    expect(page.get_by_placeholder('name@abtasty.com')).to_be_visible()
    expect(page.get_by_test_id('caretLeftIconV2')).to_be_visible()


@pytest.mark.positive
def test_return_from_reset_psw_page(page):
    """
    **Проверка возвращения на основную страницу входа со страницы восстановления пароля**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * переходим на страницу восстановления пароля
    * проверяем возвращение на основную страницу входа по ссылке на текущей странице

    Ожидаемый результат:

    * успешное возвращение на основную страницу входа
    """
    page, lang = page
    page.get_by_test_id('resetPasswordLink').click(position={'x': 10, 'y': 10})
    page.wait_for_url('**/reset-password')

    page.get_by_test_id('caretLeftIconV2').click()
    page.wait_for_url('**/login')
    expect(page).to_have_url('https://auth.abtasty.com/login')
