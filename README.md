# Торговый бот для продажи рыбы (рыбов)

Учебный проект курсов веб-разработчиков [dvmn](https://dvmn.org).  
Бот в телеграм: @devman_quiz_bot_bot.

## Установка
Вам понадобится установленный Python 3.8+ и git.

Склонируйте репозиторий:
```bash
git clone git@github.com:IlyaG96/beautiful-fish.git
```

Создайте в этой папке виртуальное окружение:
```bash
cd beautiful-fish
python3 -m venv env
```

Активируйте виртуальное окружение и установите зависимости:
```bash
source env/bin/activate
pip install -r requirements.txt
```
Или запустите приложение, используя Docker:
```shell
docker build -t beautiful-fish .
docker run --rm -v 'pwd' -d beautiful-fish
```

## Настройка перед использованием

### Переменные окружения

Перед использованием вам необходимо заполнить .env.example файл или иным образом передать переменные среды:
* TG_TOKEN - токен бота Telegram. Можно получить у [@BotFather](https://t.me/BotFather).
* REDIS_HOST - публичный адрес базы данных Redis
* REDIS_PORT - порт БД Redis
* REDIS_PASSWORD - пароль БД Redis
* ELASTIC_CLIENT_ID - id клиента [elasticpath.com](https://www.elasticpath.com)
* ELASTIC_CLIENT_SECRET - секретный ключ клиента [elasticpath.com](https://www.elasticpath.com)

## Использование


### Телеграм-бот

Бот представляет из себя торговый автомат для продажи рыбы. На данный момент можно добавить рыбу в корзину и убрать рыбу из корзины. 

Для старта телеграм-бота, запустите скрипт:
```bash
$ python bot
```

### elastic_api.py
<details>
<summary>Открыть описание</summary>


* Используются для работы с API [elasticpath.com](https://www.elasticpath.com)
* [API](https://documentation.elasticpath.com)
</details>

