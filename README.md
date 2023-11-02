# Веб-сервер со счетчиком посещений на aiohttp

Этот проект представляет собой простой веб-сервер, реализованный с 
использованием библиотеки aiohttp в Python. Сервер ведет учет посещений
страницы и уникальных посетителей, предоставляя API для получения статистики
посещений за день, месяц, год и общее количество, а также уникальных посещений
за те же периоды. Данные сохраняются в формате JSON.

## Как работает сервер

Сервер отслеживает общее количество посещений, количество уникальных 
посетителей, посещения по дням, месяцам и годам. Он обновляет счетчики при 
каждом запросе к корневому маршруту ("/").

## Установка и запуск

1. Установите необходимые зависимости, выполнив команду:

    ```bash
    pip install aiohttp
    ```

2. Запустите сервер, выполните команду:

    ```bash
    python server.py
    ```

## Эндпоинты

- `GET /` - возвращает HTML страницу с общими счетчиками посещений за день, 
 месяц и год.
- `GET /statistics` - возвращает JSON-объект со статистикой посещений.

## Структура проекта

- `clean_statistics.json` - файл с "чистой" статистикой, в котором хранится 
  количество уникальных посетителей.
- `dirty_statistics.json` - файл с "грязной" статистикой, который хранит 
  списки уникальных посетителей.

## Автор

Автор: [Илья Ратушный]