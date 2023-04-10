**SamberiPriceChecker** - простое Django-приложение для отслеживания динамики цен на сайте https://shop.samberi.com/. В качестве БД - Postgres, Celery + Redis для ежедневного парсинга. Каждый день (в 3:00 по GMT+10) будут добавляться новые данные о ценах. Отслеживать динамику изменения цен можно будет по графикам.

### **Для запуска из виртуального окружения:**

#### Требования: 

- активная бд Postgres и Redis-сервер

#### Подготовка:

- Установить зависимости командой `pip install -r requirements.txt`
- Создать файл `.env` со следующим набором переменных:
  + **DJANGO_SK** - секретный ключ Django.
  + **POSTGRES_USER** - юзер postgres (по умолчанию: **postgres**).
  + **POSTGRES_PASSWORD** - пароль postgres (по умолчанию: **postgres**).
  + **POSTGRES_DB** - база данных, к которой будет подключаться приложение (по умолчанию: **sbpc**).
  + **POSTGRES_HOST** - хост Posgres (по умолчанию: **localhost**).
  + **POSTGRES_PORT** - порт Postgres (по умолчанию: **5432**).
  + **REDIS_HOST** - хост Redis (по умолчанию: **localhost**).
  + **REDIS_PORT** - порт Redis (по умолчанию: **6379**).
  + **REDIS_DB** - БД Redis (по умолчанию: **0**)

#### Запуск:

Основное приложение: `manage.py runserver`
Celery-воркер: `celery -A SamberiPriceCheckerProject worker -l info -B`

#### Для проверки работоспособности парсера цен при поднятом сервере и работающем celery-воркере выполните следующие команды:

```
manage.py shell
from pricechecker.tasks import parse_data
parse_data.delay()
```
Если все работает корректно, то последняя команда передаст таск на выполнение Celery и через некоторое время новые цены спарсятся в БД.

### **Для запуска из docker-контейнера:**

#### Требования:

 - Установленный в системе **docker**, активная бд **Postgres** и **Redis**-сервер

#### Подготовка:

- Установить **python-dotenv** командой `pip install python-dotenv`.
- Создать файл `.env` со следующим набором переменных:
  + **DJANGO_SK** - секретный ключ Django.
  + **POSTGRES_USER** - юзер postgres (по умолчанию: **postgres**).
  + **POSTGRES_PASSWORD** - пароль postgres (по умолчанию: **postgres**).
  + **POSTGRES_DB** - база данных, к которой будет подключаться приложение (по умолчанию: **sbpc**).
  + **POSTGRES_HOST** - хост Posgres (по умолчанию: **localhost**).
  + **POSTGRES_PORT** - порт Postgres (по умолчанию: **5432**).
  + **REDIS_HOST** - хост Redis (по умолчанию: **localhost**).
  + **REDIS_PORT** - порт Redis (по умолчанию: **6379**).
  + **REDIS_DB** - БД Redis (по умолчанию: **0**)
- Создать docker-образ командой `docker build . -t sbpc_app` (имя образа на ваше усмотрение).

#### Запуск:
Пример команды для запуска контейнера `docker run --name sbpc_app -p 8000:8000 sbpc_app`


### Для запуска docker compose из приложенного docker-compose.yml:
#### Требования:

 - Установленный в системе **docker**.

#### Подготовка:
  - Создать файл `.env` со следующим набором переменных:
    + **DJANGO_SK** - секретный ключ Django.
    + **POSTGRES_USER** - юзер postgres (по умолчанию: **postgres**).
    + **POSTGRES_PASSWORD** - пароль postgres (по умолчанию: **postgres**).
    + **POSTGRES_DB** - база данных, к которой будет подключаться приложение (по умолчанию: **sbpc**).
    + **POSTGRES_HOST=db**
    + **POSTGRES_PORT=5432** 
    + **REDIS_HOST=redis**
    + **REDIS_PORT=6379**
    + **REDIS_DB=0**
    + **DB_VOLUME** - том, в котором будет хранится ваша бд.
    + **APP_PORT** - порт, на котором будет висеть приложение (по умолчанию: **8000**)
 - Создать docker-образ командой `docker build . sbpc_app`

#### Запуск:
  `docker compose up`
  













