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
+ 
+ 
+ 

### Алгоритм запуска
1. 
2.
3.
4.
5.
