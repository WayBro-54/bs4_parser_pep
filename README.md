# Проект основан на курсе обучения practicum.yandex


### О проекте 
Проект представляет собой парсер веб-сайта python.org. В рамках которого было реализованно четыре парсера. С 2 видами ражима работ и 3 способа вывода данных.

# Используемые технологии
* [Python](https://www.python.org/)
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
* [Requests Cache](https://requests-cache.readthedocs.io/en/stable/)

# Установка проекта
Склонируйте проект на локальную машину.
```sh
    git@github.com:WayBro-54/bs4_parser_pep.git 
```

# Установка виртуального окружения и зависимостей
Создаем виртуальное окружение в папке проекта.
```sh
  python -m venv venv # Для пользователей Windows
  python3 -m venv venv # Для пользователей Linux
```
Активируйте виртуальное окружение
```sh
  venv/scripts/activate # Для пользователей Windows
  venv/bin/activate # Для пользователей Linux
```
Устанавливаем зависимости
```sh
  pip install -r requirements.txt
```

## Запуск программы

# Опции которые которые имеет программа
выполните команду
```sh
  python3 main.py -h 
```
Получим описание параметров
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

options:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
- <b>whats-new</b>: - что нового. Будет выполнен парсинг последних новостей с эндпойнта https://docs.python.org/3/whatsnew/. Вывод возможен в терминал и в файл, в зависимости от выбранного режима (см. ниже)
- <b>latest-versions</b> - последние версии. Выполняет парсинг информации о версиях Python. Вывод результата возможен в терминал или файл (см. ниже)
- <b>download</b> - выполняет загрузку архива документации python в формате pdf (A4). Архив загружается в папку /downloads.
- <b>pep</b> - выполняет парсинг эндпойнта https://peps.python.org/. Выводит информацию о статусе pep и их количестве. Вывод результата возможен в терминал и файл.

- <b>-h</b>: Справка о проекта 
- <b>-c</b>: Отчистка кеша. Параметр по умолчанию сохраняет данные в кеш, для актуализации необходимо задать параметр -c 
- <b>-o</b>: Способ выводв информации. Параметр <b>-o</b> не обязателен, имеет 2 свойста <b>pretty</b> выводит данные в консоль в виде таблицы, <b>file</b> Выводит данные в файл в дирректории <b>results</b>. Дефолтный вывод даннных осуществляется в консоль.


