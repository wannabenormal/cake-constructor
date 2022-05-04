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
<summary>Подробнее</summary>

- Создайте файл `.env` в той же папке, что и `manage.py` или заполните прилагающийся `.env.example` и переименуйте его в `.env`:
```shell
STRIPE_PUBLIC_KEY=""
STRIPE_SECRET_KEY=""
DEBUG=""
ALLOWED_HOSTS=""
SECRET_KEY=""
```
- `STRIPE_PUBLIC_KEY` - публичный ключ платежной системы [stripe](https://stripe.com)
- `STRIPE_SECRET_KEY` - секретный ключ платежной системы [stripe](https://stripe.com)
- `DEBUG` - дебаг-режим. Поставьте `False`.
- `SECRET_KEY` - секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Не стоит использовать значение по-умолчанию, **замените на своё**.
- `ALLOWED_HOSTS` - [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

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

### API
<details>
<summary>Подробнее</summary>

Возможное количество этажей `height` торта: 

- one - один
- two - два
- three - три

Возможные формы `shape` тортов:
- c - круг
- s - квадрат
- r - прямоугольник

Возможные топпинги `topping` для тортов:

- without - без топиинга
- white_sauce - белый соус
- caramel - каамельный
- maple - кленовый сироп
- blueberry - голубика
- white_choco - белый шоколад

Возможные ягоды `berry` для тортов:

- without - без ягод
- bramble - ежевика
- rasp - малина
- blue - голубика
- straw - клубника


Возможные украшения `decodation` для тортов:

- without - без
- pistachio - с фисташками
- bese - безе
- hazelnut - лесной орех
- pecan - пекан
- marsh - маршмеллоу
- marzipan - марципан


Пример корректного json-запроса к Api:

```json
{"delivery_datetime": "2022-04-28 01:08:49.016151",
  "delivery_address": "Москва",
  "customer": {
    "name": "first",
    "email": "validated@mail.ru",
    "phonenumber": "+79870608786",
    "address": "Москва"},
  "cake": {"name": "Cake",
    "description": "simple cake",
    "height": "one",
    "shape": "s",
    "topping": "without",
    "berry": "without",
    "decoration": "without",
    "inscription": ""}}
```
-- "delivery_datetime": дата доставки, обязательное поле `datetime`  
-- "delivery_address": адрес доставки, обязательное поле, `str`

- `customer`

-- "name": имя заказчика, обязательное поле, `str`  
-- "email": электронная почта заказчика, обязательное поле `str`  
-- "phonenumber": номер телефона заказчика, обязательное поле `phonenumberfield`  
-- "address": ардес заказчика, обязательное поле `str`  
-- "comment": комментарий к заказу, необязательное поле, `str`  
- `cake`  

-- "name": название торта, необязательное поле, `str`    
-- "description": описание торта, необязательное поле, `str`  
-- "height": описание торта, необязательное поле, `str`  
-- "shape": форма торта, необязательное поле, `str`  
-- "topping": топпинг для торта, необязательное поле, `str`  
-- "berry": ягоды для торта, необязательное поле, `str`  
-- "decoration": декорация торта, необязательное поле, `str`  
-- "inscription": надпись на торте, необязательное поле, `str`  

[создать заказ](http://127.0.0.1:8000/register_order)

</details>

