

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import schedule
from datetime import datetime


def get_book_data(book_url: str) -> pd.DataFrame:

    """
    НАЗНАЧЕНИЕ ФУНКЦИИ
    ------------------
    парсинг характеристик книги с сайта books.toscrape.com
    Функция получает URL страницы книги --> извлекает её характеристики (название, описание, UPC, цену, наличие и др. параметры)  -->  возвращает их в виде DataFrame

    ВХОДНЫЕ ПАРАМЕТРЫ
    ----------
    book_url : str
    Полный URL страницы книги на сайте books.toscrape.com. Пример: 'http://books.toscrape.com/catalogue/book-name_123/index.html'

    ВЫХОДНЫЕ ЗНАЧЕНИЯ
    -------
    + pd.DataFrame or None
        DataFrame с двумя колонками:
        - 'Parameter': названия характеристик книги (индекс)
        - 'Value': значения характеристик
        
    + None, если book_url не передан или произошла ошибка

    ОКРУЖЕНИЕ
    ---------
    библиотеки: 
        + requests: обращение к ресурсам по HTTP
        + BeautifulSoup: парсинг HTML
    """

    if book_url:
        response = requests.get(book_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Название книги
            title = soup.find("title").text.strip()

            # Описание книги
            description_div = soup.find("div", id="product_description")
            if description_div:
                description = description_div.find_next_sibling("p").text.strip()
            else:
                description = "No description available"

            # Таблица характеристик книги
            product_information = soup.find("table", class_="table-striped")
            
            # словарь атрибутов книги
            attribute_books = {}
            attribute_books["Title"] = title
            attribute_books["Description"] = description

            if product_information:
                for row in product_information.find_all("tr"):
                    attribute_books[row.find("th").text.strip()] = row.find("td").text.strip()

            charasteristics_book_df = pd.DataFrame(
                data={"Parameter": attribute_books.keys(), "Value": attribute_books.values()}
            )
            charasteristics_book_df.set_index("Parameter", inplace=True)

            return charasteristics_book_df
    
    return None


def scrape_books(is_save_to_file: bool = False):

    """
    НАЗНАЧЕНИЕ ФУНКЦИИ
    ------------------
    парсит каталог книг с сайта books.toscrape.com
    Функция последовательно обходит все страницы каталога книг, (начиная с первой страницы)
    Для каждой найденной книги вызывается функция get_book_data(book_url) для извлечения детальной информации
    Результаты могут быть сохранены в текстовый файл

    ВХОДНЫЕ ПАРАМЕТРЫ
    ----------
    is_save_to_file : bool, optional
        Флаг сохранения результатов парсинга в файл (default is False)
        - True: сохраняет данные в файл 'books_data.txt' в текущей директории
        - False: файл не создается, данные возвращаются только как результат функции

    ВЫХОДНЫЕ ЗНАЧЕНИЯ
    ------------------
    list of pd.DataFrame: cписок DataFrame'ов, где каждый элемент содержит характеристики одной книги. Каждый DataFrame имеет структуру, возвращаемую функцией get_book_data() 

     ОБРАБОТКА ОШИБОК И ИСКЛЮЧЕНИЙ
    ------------------------------
    Exception
    При ошибках сетевых запросов или парсинга HTML выводится сообщение об ошибке, но выполнение функции продолжается со следующей страницы

    ПРИМЕЧАНИЯ
    ----------
    - функция автоматически определяет последнюю страницу каталога
    - между запросами добавлена задержка 0.2 секунды для снижения нагрузки на сервер
    """

    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    catalogue_url = "http://books.toscrape.com/catalogue/"
    
    all_books_data = []
    page_number = 1
    
    print("Начинаем парсинг каталога книг...")
    
    while True:
        
        # Формируование url страницы каталога
        page_url = base_url.format(page_number)
        print(f"\nПарсинг страницы {page_number}: {page_url}")
        
        try:
            response = requests.get(page_url)
            
            # Если страница не найдена, значит, каталог закончился
            if response.status_code != 200:
                print(f"Страница {page_number} не найдена. Парсинг завершен.")
                break
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Нахожу все книги на странице
            books = soup.find_all("article", class_="product_pod")
            
            if not books:
                print("Книги не найдены. Парсинг завершен.")
                break
            
            print(f"Найдено {len(books)} книг на странице {page_number}")
            
            # Парсинг каждой книги
            for idx, book in enumerate(books, 1):
                # Получаем ссылку на страницу книги
                book_link = book.find("h3").find("a")["href"]
                
                # Формируем полный URL книги
                book_url = catalogue_url + book_link.replace("../", "")
                
                print(f"  Парсинг книги {idx}/{len(books)}: {book_url}")
                
                # Получаем данные книги
                book_data = get_book_data(book_url)
                
                if book_data is not None:
                    all_books_data.append(book_data)
                
                # Небольшая задержка, чтобы не перегружать сервер
                time.sleep(0.2)
            
            # Переход к следующей странице
            page_number += 1
            
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_number}: {e}")
            break
    
    print(f"\n{'='*60}")
    print(f"Парсинг завершен! Всего собрано данных о {len(all_books_data)} книгах.")
    print(f"{'='*60}")
    
    # Сохранение в файл (если требуется)
    if is_save_to_file and all_books_data:
        filename = "books_data.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            for i, book_df in enumerate(all_books_data, 1):
                f.write(f"\n{'='*60}\n")
                f.write(f"КНИГА #{i}\n")
                f.write(f"{'='*60}\n\n")
                f.write(book_df.to_string())
                f.write("\n")
        
        print(f"\nДанные успешно сохранены в файл: {filename}")
    
    return all_books_data


def scheduled_scraping():
    """
    НАЗНАЧЕНИЕ ФУНКЦИИ
    ------------------
    функция-обертка для запуска парсера по расписанию;
    выводит информацию о времени запуска и вызывает scrape_books с сохранением результатов в файл.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'#'*70}")
    print(f"# ЗАПУСК ЗАПЛАНИРОВАННОГО ПАРСИНГА")
    print(f"# Время запуска: {current_time}")
    print(f"{'#'*70}\n")
    
    try:
        scrape_books(is_save_to_file=True)
        print(f"\n{'#'*70}")
        print(f"# ПАРСИНГ ЗАВЕРШЕН УСПЕШНО")
        print(f"# Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}\n")
    except Exception as e:
        print(f"\n{'#'*70}")
        print(f"# ОШИБКА ПРИ ПАРСИНГЕ: {e}")
        print(f"{'#'*70}\n")


def run_scheduler(schedule_time: str = "19:00"):
    """
    НАЗНАЧЕНИЕ ФУНКЦИИ
    ------------------
    запускает планировщик задач для автоматического парсинга;
    Функция настраивает ежедневный запуск парсинга в указанное время и запускает бесконечный цикл ожидания с проверкой расписания
    
    ВХОДНЫЕ ПАРАМЕТРЫ
    -----------------
    schedule_time : str, optional
        Время запуска в формате "HH:MM" (default is "19:00").
        Примеры: "19:00", "09:30", "15:45"
    
    ПРИМЕЧАНИЯ
    ----------
    - цикл проверяет расписание каждую минуту
    - программа работает до принудительной остановки. Команда: Ctrl+C)
    - при каждом запуске выводится информация о времени выполнения
    - результаты автоматически сохраняются в файл "books_data.txt"
    """
    # Настройка расписания
    schedule.every().day.at(schedule_time).do(scheduled_scraping)
    
    print(f"\n{'*'*70}")
    print(f"* ПЛАНИРОВЩИК ЗАПУЩЕН")
    print(f"* Запланированное время выполнения: каждый день в {schedule_time}")
    print(f"* Текущее время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"* Для остановки нажмите Ctrl+C")
    print(f"{'*'*70}\n")
    
    # Вывод времени следующего запуска
    next_run = schedule.next_run()
    if next_run:
        print(f"Следующий запуск запланирован на: {next_run.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Бесконечный цикл выполнения задач по расписанию
    try:
        while True:
            # Проверяем, нужно ли выполнить задачу
            schedule.run_pending()
            
            # Ожидаем 60 секунд перед следующей проверкой
            # Это снижает нагрузку на систему
            time.sleep(60)
            
    except KeyboardInterrupt:
        print(f"\n{'*'*70}")
        print(f"* ПЛАНИРОВЩИК ОСТАНОВЛЕН ПОЛЬЗОВАТЕЛЕМ")
        print(f"* Время остановки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'*'*70}\n")


if __name__ == "__main__":
    
    # --------------------------------------------------
    # Тест_1: запуск по расписанию (в 19:00 каждый день)
    # --------------------------------------------------
    run_scheduler(schedule_time="19:00")
    
    # ----------------------------
    # Тест_2: запуск через N минут
    # ----------------------------
    # from datetime import timedelta
    # test_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    # print(f"ТЕСТ_2: запуск запланирован через 1 минуту - в {test_time}")
    # run_scheduler(schedule_time=test_time)
    
    # --------------------------
    # Тест_2: однократный запуск
    # --------------------------
    # scrape_books(is_save_to_file=True)