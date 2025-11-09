# Скрайпер каталога книг
Парсинг каталога книг с веб-ресурса books.toscrape.com

## Описание проекта
python-скрипт для парсинга характеристик каталога книг по расписанию.

### Характеристики книг
+ Title: название книги
+ Description: описание
+ UPC: универсальный код товара
+ Price: цена
+ Availability: наличие на складе
+ Rating: рейтинг
+ Number of reviews: количество отзывов
+ Product Type: тип товара
+ Price (excl.tax): цена без налога
+ Price (incl.tax): цена с налогом
+ Tax: налог


## Стек.Библиотеки
+ requests http-запросы к веб-серверу
+ BeatifulSoup4: парсинг html-страниц
+ Pandas: упаковка и обработка данных
+ schedule: планирование задач по расписанию

## Структура проекта
```
hw3_books_scraper_data/
|
# основной файл проекта
|-- scraper.py
# документация проекта
|-- README.md
# перечень зависимостей
|-- requirements.txt
# игнорируемые Git'ом файлы
|-- .gitignore
|  # скрайпинг данных по книге
|  |-- get_book_data{}
|   # скрайпинг каталога книг
|  |-- scrape_books()
|  # обертка для запуска парсера по расписанию
|  |-- scheduled_scraping()
|  # планировщик
|  |-- run_scheduler()
|  # Jupyter Notebook + .py
|-- notebooks/
|  |- HW 03 Python DS 2025 .ipynb
|  |- worker.py
|-- artifacts/
|  # документ со ссылкой на Google Drive с артефактами
|  |- artifacts.txt
```
## Запуск проекта

### Окружение
+ Python >= 3.8
+ pip
+ Git

### Алгоритм запуска
1. клонировать репозиторий
```
git clone https://github.com/ваш-username/books_scraper.git
cd books_scraper
```
2. Собрать venv
```
# WINDOWS
git clone https://github.com/ваш-username/books_scraper.git
cd books_scraper

Linux/ MacOS
python3 -m venv venv
source venv/bin/activate
```
3. Установить зависимости
```
pip install -r ewquirements.txt
```
4.1 Запустить парсер: однократный старт
```
python scraper.py
"""
результат:
файл books_data.txt сохраняется в директорию artifacts
"""
```

4.2 Запустить парсер по расписанию
```
4.2.1 открыть
scraper.py

4.2.2.1 расскомментить выражение
 run_scheduler(schedule_time="19:00")
4.2.2.2 закомментить однократный тест

4.2.1 запустить
python scraper.py
"""
результат:
скрипт начнет периодическую проверку целевого времени (19.00) и приступит к нему ровно в 19.00
"""
```

4.3 Запустить парсер через 60 секунд
```
4.3.1 запустить
scraper.py
```
