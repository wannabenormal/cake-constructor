# Сайт "Cake-constructor"

Учебный проект для курсов web-разработчиков [dvmn](https://dvmn.org).  
Cайт можно посетить, если нажать [сюда](http://websitesitesite.comru).

## Установка
- Понадобится установленный Python 3.8+ и git.

- Склонируйте репозиторий:
```bash
git@github.com:wannabenormal/cake-constructor.git
```
- Создайте виртуальное окружение:
```bash
cd cake-constructor
python3 -m venv env
```

- Активируйте виртуальное окружение и установите все необходимые пакеты.
```bash
source env/bin/activate
pip install -r requirements.txt
```
- Возможно, потребуется обновить pip командой:
```shell
python3 -m pip install --upgrade pip
```
## Вероятные сценарии использования

### Протестировать сайт локально
<details>
<summary>Протестировать сайт локально</summary>

- Создайте файл `.env` в той же папке, что и `manage.py` или заполните прилагающийся `.env.example` и переименуйте его в `.env`:
```shell
SECRET_KEY=paste_your_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
```
SECRET_KEY - секретный ключ проекта Django.  
DEBUG - режим отладки (стандартно- True).  
ALLOWED_HOSTS - ip адрес вашего сервера. По умолчанию: 127.0.0.1.
- Скачайте фронтенд [по ссылке](https://disk.yandex.ru/d/lT3TxLcBjWvrYA)
- ### инструкция по настройке фронта
- Создайте базу данных командой:
```shell
python manage.py migrate
```
- Создайте суперпользователя (админа).
```shell
python manage.py createsuperuser
```
- Запустите сервер локально.
```shell
python manage.py runserver
```

</details>

