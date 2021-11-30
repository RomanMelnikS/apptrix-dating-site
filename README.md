# apptrix-dating-site

Проект развёрнут и доступен для ознакомления здесь https://safe-waters-89972.herokuapp.com/api/list/

Admin:
- ad@ad.ru
- admin

### Авторизация:
- Переходим на /api/clients/token/login/ вводим необходимые данные.
- Получаем "access": "token" и "refresh": "token"
- В запросах передаём Headers: Authorization: Bearer {"accsess"}
- Если срок действия токена истёк, переходим на /api/clients/token/refresh/ и передаём refresh: "refresh"
- Получаем обновлённый "access": "token"

### Endpoints:
#### /api/clients/create/ [POST]: Cоздаёт пользователя:
Поля:
- email - [str] - required
- username - [str] - required
- password - [str] - required
- first_name - [str]
- last_name - [str]
- sex - [choice] ["м", "ж"] - required
- avatar - [Base64image] - required
- location - [{longitude: [int], latitude: [int]}] - required

#### /api/clients/token/login/ [POST]: Cоздаёт token для авторизации пользователя:
Поля:
- email - [str] - required
- password - [str] - required

#### /api/clients/token/refresh/ [POST]: Обновляет token для авторизации пользователя:
Поля:
- refresh - [str] - required

#### /api/clients/{id}/match/ [POST] [Authenticated]: Создаёт симпатию к пользователю и отправляет уведомление на Email, если она взаимная:
Аргументы:
- id - [int] (идентификатор пользователя)

#### /api/list/ [GET]: Список всех пользователей:
Фильтры:
- ?sex= 
- ?first_name=
- ?last_name=
- ?location= (пока работает не так как должен, отображает пользователей у которых указана локация, доступен только авторизованым пользователям) 



### Локальный запуск проекта.
1. Откройте терминал и перейдите в ту директорию, в которой будет располагаться проект.
2. Склонируйтуе проект к себе на машину:
```python
git clone https://github.com/RomanMelnikS/apptrix-dating-site.git
```
3. Перейдите в корневую директорию проекта создайте и активируйте виртуальное окружение:
```python
python -m venv 'venv'
source venv/Scripts/activate
pip install requirements.txt
```
4. В директории backend/, создайте .env файл со следующими переменными:
    - SECRET_KEY - Секретный ключ Django
    - DEBUG - 1
    - EMAIL - Ваш почтовый хост @yandex.ru
    - EMAIL_PASSWOR - Пароль от почтового хоста
5. В backend/settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
6. Перейдите в директорию backend/ и выполните команды:
```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Проект запустится локально на вашей машине и будет доступен по ссылке http://127.0.0.1:8000/.
