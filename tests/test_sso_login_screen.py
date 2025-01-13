from os import linesep as ls

import pytest
from playwright.sync_api import expect


@pytest.mark.layout
def test_sso_page_elements(page):
    """
    **Проверка элементов на странице входа по SSO**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * переходим на страницу входа по SSO
    * проверяем URL, title, заголовок, название страницы
    * проверяем наличие интерактивных элементов: полей ввода, кнопок и ссылок
    * проверяем наличие статических элементов верстки на странице

    Ожидаемый результат:

    * элементы отображаются в соответствии с требованиями дизайна
    """
    page, lang = page
    page.get_by_test_id('ssoLoginButton').click()

    page.wait_for_url('**/ssologin*')
    expect(page).to_have_url('https://auth.abtasty.com/ssologin?return_to=https%3A%2F%2Fapp2.abtasty.com')
    expect(page).to_have_title('AB Tasty - Experience Optimization Platform')
    expect(page.get_by_role("link", name="abtasty")).to_be_visible()
    expect(page.get_by_role('heading', name='Sign in With SSO')).to_be_visible()

    expect(page.locator('#email')).to_be_visible()
    expect(page.get_by_role('button', name='Sign In')).to_be_visible()
    expect(page.get_by_role('link', name='Go back to Login page')).to_be_visible()
    expect(page.get_by_role('link', name='Learn more about single sign-on')).to_be_visible()

    expect(page.get_by_text('E-mail')).to_be_visible()
    expect(page.get_by_placeholder('name@abtasty.com')).to_be_visible()
    expect(page.get_by_test_id('caretLeftIconV2')).to_be_visible()


@pytest.mark.positive
def test_return_from_sso_page(page):
    """
    **Проверка возвращения на основную страницу входа со страницы входа по SSO**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * переходим на страницу входа по SSO
    * проверяем возвращение на основную страницу входа по ссылке на текущей странице

    Ожидаемый результат:

    * успешное возвращение на основную страницу входа
    """
    page, lang = page
    page.get_by_test_id('ssoLoginButton').click()
    page.wait_for_url('**/ssologin*')

    page.get_by_test_id('caretLeftIconV2').click()
    page.wait_for_url('**/login')
    expect(page).to_have_url('https://auth.abtasty.com/login')


@pytest.mark.negative
def test_non_existent_user_email_sso(page):
    """
    **Проверка сообщения о несуществующем email пользователя на странице входа по SSO**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * переходим на страницу входа по SSO
    * проверяем отсутствие сообщения об ошибке email до начала ввода
    * проверяем, что кнопка ВХОД активна до начала ввода
    * заполняем поле email соответствующим по формату стандарту email, но для не несуществующего в SSO пользователя
    * нажимаем кнопку ВХОД
    * проверяем что кнопка ВХОД неактивна (на время запроса)
    * проверяем наличие сообщения об ошибке в поле email

    Ожидаемый результат:

    * сообщение об ошибке появляется в соответствии с требованиями
    """
    page, lang = page
    page.get_by_test_id('ssoLoginButton').click()
    page.wait_for_url('**/ssologin*')

    expect(page.get_by_test_id('emailErrorMessage')).not_to_be_visible()
    expect(page.get_by_role('button', name='Sign In')).to_be_enabled()
    page.fill('#email', 'conformed@email.com')
    page.get_by_role('button', name='Sign In').click()

    expect(page.locator('button[type="submit"]')).to_be_disabled()
    expect(page.get_by_test_id('emailErrorMessage')).to_be_visible()
    expect(page.get_by_text('Please enter a valid email')).to_be_visible()
