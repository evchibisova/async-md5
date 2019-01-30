Для установки библиотек из requirements.txt выполните в командной строке:
>pip install -r requirements.txt

Для отправки пользователю e-mail с MD5 и URL файла запишите в email_data.txt через пробел почтовый адрес отправителя, пароль и параметры smtp-сервера.
Например, для mail.ru:
sender@mail.ru password smtp.mail.ru 465

Для запуска сервера выполните:
> python -m aiohttp_server.py

Сервер запустится по адресу localhost:8000
