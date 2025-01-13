Установить библиотеки:
-
- Python >=3.12 
```
pip install -r requirements.txt
```
Установить браузер(ы) Playwright
- 
- Localhost:
```
playwright install --with-deps --force chromium
```
- CI:
```
playwright install --with-deps --force --only-shell chromium
```
Запуск pytest:
-
- Localhost: `pytest`
  - запуск тестов с фильтром по маркерам, установленным в файле `pytest.ini`:
```
pytest -m <marker1> ... <markerN>
```
  - - для просмотра всех маркеров: `pytest --markers`

- - запуск в [режиме отладки с Playwright Inspector](https://www.browserstack.com/guide/playwright-debugging#:~:text=To%20launch%20your%20test%20with,using%2C%20the%20syntax%20might%20differ.&text=Once%20you%20enter%20the%20command,the%20line%20is%20being%20executed):
    - Bash:         `PWDEBUG=1 pytest test_<filename>.py`
    - PowerShell:
```
$env:PWDEBUG=1` `pytest test_<filename>.py`
```
- CI:
```
python -m pytest -m <marker1> ... <markerN>
```
Отчеты:
   -
   - на данном этапе реализации предусмотрен отчет в stdout

Документация:
   -
   - Ссылка на требования: в папке проекта \DOC
   - Описание тестового покрытия и тестовые сценарии: в едином файле проекта \DOC\singlehtml\index.html
   - команда для обновления документации:
```
.\make.bat singlehtml
```
- - или интерактивного вывода в файле проекта \DOC\html\index.html
```
python -m sphinx .\tests .\DOC\html
```
