import pytest, pytest_asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright, BrowserContext, Page


@pytest_asyncio.fixture(scope="session")
async def browser_async() -> BrowserContext:
    """
    Настройки размера окна асинхронного браузера
    :return: context
    """
    viewport_width = 1024
    viewport_height = 800

    async with async_playwright() as pw:
        # Запускаем браузер с заданными размерами окна
        # - установить `headless=True`, если не хотим видеть браузер
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height}
        )
        yield context
        await context.close()
        await browser.close()


@pytest.fixture(scope='session')
def browser():
    """
    Настройки размера окна синхронного браузера
    :return: context
    """
    viewport_width = 1024
    viewport_height = 800

    with sync_playwright() as pw:
        # Запускаем браузер с заданными размерами окна
        # - установить `headless=True`, если не хотим видеть браузер
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height}
        )
        yield context
        context.close()
        browser.close()


@pytest_asyncio.fixture(scope='function')
async def page_async(browser_async: BrowserContext) -> Page:
    """
    Открывает новую страницу в контексте асинхронного браузера
    определяет локализацию языка страницы
    :returns: tuple(page, lang)
    """
    page = await browser_async.new_page()
    await page.goto('https://app2.abtasty.com/login')
    lang = await page.locator('html').get_attribute('lang')
    yield page, lang
    await page.close()


@pytest.fixture(scope='function')
def page(browser):
    """
    Открывает новую страницу в контексте синхронного браузера
    определяет локализацию языка страницы
    :returns: tuple(page, lang)
    """
    page = browser.new_page()
    page.goto('https://app2.abtasty.com/login')
    lang = page.locator('html').get_attribute('lang')
    yield page, lang
    page.close()
