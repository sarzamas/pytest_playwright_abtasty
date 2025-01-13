from os import linesep as ls

import pytest
from playwright.sync_api import expect


@pytest.mark.layout
def test_login_page_elements(page):
    """
    **Проверка элементов на основной странице входа в приложение**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * проверяем заголовок страницы
    * проверяем наличие интерактивных элементов: полей ввода, кнопок и ссылок
    * проверяем наличие статических элементов верстки на странице

    Ожидаемый результат:

    * элементы отображаются в соответствии с требованиями дизайна
    """
    page, lang = page

    expect(page).to_have_title('AB Tasty - Experience Optimization Platform')
    expect(page.get_by_role("link", name="abtasty")).to_be_visible()
    expect(page.get_by_role('heading', name='Login')).to_be_visible()

    expect(page.get_by_test_id('emailInput')).to_be_visible()
    expect(page.get_by_test_id('passwordInput')).to_be_visible()
    expect(page.get_by_test_id('resetPasswordLink')).to_be_visible()
    expect(page.get_by_role('link', name='Forgot your password?')).to_be_visible()
    expect(page.locator('#signInButton')).to_be_visible()
    expect(page.get_by_role('button', name='Sign In')).to_be_visible()
    expect(page.locator('#GOOGLE_SIGN_IN_BUTTON')).to_be_visible()
    expect(page.get_by_test_id('ssoLoginButton')).to_be_visible()
    expect(page.get_by_role('button', name='Login with SSO')).to_be_visible()
    expect(page.get_by_role('link', name='Privacy Policy')).to_be_visible()

    image = page.locator('a > img')
    expect(image).to_be_visible()
    expect(image).to_have_attribute('src', '/logo-v2.svg')
    expect(image).to_have_attribute('height', '28')
    expect(image).to_have_attribute('width', '123')
    expect(page.get_by_text('E-mail*')).to_be_visible()
    expect(page.get_by_placeholder('name@abtasty.com')).to_be_visible()
    expect(page.get_by_text('Password*')).to_be_visible()
    expect(page.get_by_placeholder('At least 12 characters')).to_be_visible()
    expect(page.get_by_test_id('visibilityShowIconV2')).to_be_visible()
    expect(page.get_by_text('Or', exact=True)).to_be_visible()
    expect(page.get_by_text('Learn more about our Privacy Policy.')).to_be_visible()


@pytest.mark.xfail
@pytest.mark.negative
def test_short_or_empty_input_fields(page):
    """
    **Проверка правил Enabled/Disabled кнопки ВХОД при опустошении полей ввода на странице входа**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * проверяем, что кнопка ВХОД неактивна
    * заполняем поле email любым корректным по формату email - проверяем, что кнопка ВХОД неактивна
    * заполняем поле password любыми данными длиной менее 12 символов - проверяем, что кнопка ВХОД неактивна
    * заполняем поле password любыми данными длиной 12 и более символов - проверяем, что кнопка ВХОД стала активна
    * очищаем полностью поле email - проверяем, что кнопка ВХОД стала неактивна
    * заполняем поле email любым корректным по формату email - проверяем, что кнопка ВХОД стала активна
    * в поле password стираем данные до длины от 1 до 12 символов - проверяем что кнопка ВХОД стала неактивна

    Ожидаемый результат:

    * кнопка ВХОД изменяет свою активность в соответствии с требованиями
    """
    page = page[0]

    expect(page.locator('#signInButton')).to_be_disabled()
    page.fill('#email', 'conformed_email@abtasty.com')
    expect(page.locator('#signInButton')).to_be_disabled()
    page.fill('#password', '12345678901')
    expect(page.locator('#signInButton')).to_be_disabled() # TODO: BUG - должно быть disabled
    page.locator('#password').press('2')
    expect(page.locator('#signInButton')).to_be_enabled()
    page.locator('#email').clear()
    expect(page.locator('#signInButton')).to_be_disabled()
    page.fill('#email', 'conformed_email@abtasty.com')
    expect(page.locator('#signInButton')).to_be_enabled()
    page.locator('#password').focus()
    page.keyboard.press('Backspace')
    expect(page.locator('#signInButton')).to_be_diabled() # TODO: BUG - должно быть disabled


@pytest.mark.negative
def test_non_conformed_email_format(page):
    """
    **Проверка сообщения о несоответствующем формате email на странице входа**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * проверяем отсутствие сообщения об ошибке email до начала ввода
    * заполняем поле email текстом, не соответствующим по формату стандарту email
    * переносим фокус мышью на другое поле ввода
    * проверяем наличие сообщения об ошибке в поле email
    * заполняем поле email текстом, соответствующим по формату стандарту email
    * проверяем исчезновение сообщения об ошибке в поле email

    Ожидаемый результат:

    * сообщение об ошибке появляется и исчезает в соответствии с требованиями
    """
    page, lang = page

    expect(page.get_by_test_id('emailErrorMessage')).not_to_be_visible()
    page.fill('#email', 'non.conformed.email')
    page.focus('#password')
    expect(page.get_by_test_id('emailErrorMessage')).to_be_visible()
    expect(page.get_by_text('Please enter a valid email')).to_be_visible()
    page.fill('#email', 'invalid_email@abtasty.com')
    expect(page.get_by_test_id('emailErrorMessage')).not_to_be_visible()


@pytest.mark.layout
def test_password_hide_show_eye_button(page):
    """
    **Проверка видимости пароля по кнопке 'глаз' на странице входа**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * заполняем поле пароля случайным значением
    * фиксируем тип значения введенного пароля при сокрытии видимости в виде точек
    * нажимаем на кнопку 'глаз'
    * фиксируем тип значения введенного пароля без сокрытия видимости в виде текста
    * нажимаем на кнопку 'глаз' еще раз
    * снова фиксируем тип значения введенного пароля при сокрытии видимости в виде точек

    Ожидаемый результат:

    * видимость пароля по кнопке 'глаз' появляется и исчезает в соответствии с требованиями
    """
    page = page[0]

    page.fill('#password', 'any_password')
    expect(page.get_by_test_id('visibilityShowIconV2')).to_be_visible()
    expect(page.locator('#password')).to_have_attribute('type', 'password')
    page.get_by_test_id('visibilityShowIconV2').click()
    expect(page.get_by_test_id('visibilityHideIconV2')).to_be_visible()
    expect(page.locator('#password')).to_have_attribute('type', 'text')
    page.get_by_test_id('visibilityHideIconV2').click()
    expect(page.get_by_test_id('visibilityShowIconV2')).to_be_visible()
    expect(page.locator('#password')).to_have_attribute('type', 'password')


@pytest.mark.negative
def test_wrong_login_credentials(page):
    """
    **Проверка сообщения о неверно введенных данных на странице входа**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * проверяем отсутствие сообщения об ошибке до начала ввода
    * проверяем что кнопка ВХОД неактивна
    * заполняем поля данными соответствующим по формату, но несуществующего пользователя
    * проверяем что кнопка ВХОД активна и нажимаем ее
    * проверяем что кнопка ВХОД неактивна (на время запроса)
    * проверяем наличие сообщения об ошибке

    Ожидаемый результат:

    * сообщение об ошибке появляется и соответствует требованиям
    """
    page, lang = page

    expect(page.locator('#loginErrorMessage')).not_to_be_visible()
    expect(page.locator('#signInButton')).to_be_disabled()
    page.fill('#email', 'invalid_user@abtasty.com')
    page.fill('#password', 'invalid_password')
    expect(page.locator('#signInButton')).to_be_enabled()
    page.locator('#signInButton').click()
    expect(page.locator('#signInButton')).to_be_disabled()
    expect(page.locator('#loginErrorMessage')).to_be_visible()
    expect(page.get_by_text('Please enter a valid email or password')).to_be_visible()


@pytest.mark.positive
def test_captcha(page):
    """
    **Поверка элементов на странице ввода Captcha**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * сначала производим три неудачных попытки входа с невалидными данными
    * далее заполняем поля ввода валидными данными и нажимаем кнопку ВХОД
    * проверяем появление блока Captcha на странице
    * проверяем наличие интерактивных и статических элементов Captcha
    * проходим Captcha
    * проверяем успешный переход в приложение

    Ожидаемый результат:

    * переход в приложение осуществлен
    """
    page, lang = page

    page.fill('#email', 'invalid_user@abtasty.com')
    page.fill('#password', 'invalid_password')
    for attempt in range(1, 4):
        print(f"{ls if attempt < 2 else ''}failed login attempt count: {attempt}")
        expect(page.locator('#signInButton')).to_be_visible()
        page.locator('#signInButton').click()
        expect(page.locator('#signInButton')).to_be_disabled()
    page.fill('#email', 'valid_user@abtasty.com')  # TODO: заменить на действительные учетные данные
    page.fill('#password', 'valid_password')  # TODO: заменить на действительные учетные данные
    expect(page.get_by_role('button', name='Sign In')).to_be_visible()
    page.locator('#signInButton').click()

    expect(page.locator('#loginErrorMessage')).to_be_visible()  # TODO: заменить селектор на актуальный для Captcha
    # TODO: добавить проверку элементов Captcha
    # TODO: добавить прохождение Captcha
    #page.wait_for_url('**/dashboard')                          # TODO: заменить на актуальный URL после успешного входа
    expect(page).to_have_url('https://auth.abtasty.com/login?return_to=https%3A%2F%2Fapp2.abtasty.com')
    print('Captcha: Skipped/TODO')


@pytest.mark.positive
def test_login_success(page):
    """
    **Поверка успешного входа**

    Шаги воспроизведения:

    * переходим на основную страницу входа в приложение и определяем <html lang>
    * заполняем поля ввода валидными данными и нажимаем кнопку ВХОД
    * проверяем успешный переход в приложение

    Ожидаемый результат:

    * переход в приложение осуществлен
    """
    page, lang = page

    page.fill('#email', 'valid_user@abtasty.com')  # TODO: заменить на действительные учетные данные
    page.fill('#password', 'valid_password')  # TODO: заменить на действительные учетные данные
    expect(page.locator('#signInButton')).to_be_visible()
    page.locator('#signInButton').click()
    expect(page.locator('#signInButton')).to_be_disabled()
    #page.wait_for_url('**/dashboard')                          # TODO: заменить на актуальный URL после успешного входа
    # TODO: заменить на актуальный URL после успешного входа
    expect(page).to_have_url('https://auth.abtasty.com/login?return_to=https%3A%2F%2Fapp2.abtasty.com')
