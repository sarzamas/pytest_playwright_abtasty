# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

"""
Инициализировать Sphinx в проекте если отсутствует `conf.py`:
```bash
sphinx-quickstart docs/
```
Генерация документации с помощью Sphinx:
 - выполнить две команды последовательно из корневой директории проекта, где находятся src/ и docs/

1. Генерация файлов .rst (шаблонов документации)
```bash
sphinx-apidoc -o docs/ src/
```
Sphinx не умеет напрямую парсить исходный код
Эта команда генерирует структуру документации, которую можно редактировать:
  - создает .rst-файлы (ReStructuredText) на основе Python-модулей в папке src/
  - сохраняет их в директорию docs/

2. Сборка HTML-документации
```bash
make html
```
Получение документации в формате веб-страниц:
  - преобразует .rst-файлы из папки docs/ в HTML-страницы
  - результат сохраняется в docs/_build/html/
"""


import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ABTasty'
copyright = '2025, sarzamas'
author = 'sarzamas'
version = '0.1'
release = '0.1.0'
year = datetime.now().year

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',      # ссылки на исходный код docstrings
    'sphinx.ext.napoleon',      # для поддержки Google и NumPy стиля docstrings
    'sphinx_autodoc_typehints', # если используете типы
]

html_static_path = ['_static']

# Логотип документации
html_logo = '_static/abtasty.svg'

# Подключить файл CSS для корректировки стилей
html_css_files = [
    'custom.css',
]

# templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# где искать тесты
autodoc_mock_imports = ['pytest']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_theme_options = {
    'page_width' : '1000px',
    'logo': 'abtasty.svg',
    'description': '',
    'description_font_style': '',
    'github_user': 'sphinx-doc',
    'github_repo': 'alabaster',
}
