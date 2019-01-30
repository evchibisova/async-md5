### Веб-сервис на aiohttp для скачивания файлов из Интернет и расчета MD5-hash файла в фоновом режиме

#### Сборка и запуск приложения

Для установки библиотек из requirements.txt выполните в командной строке:
>pip install -r requirements.txt

Для отправки пользователю e-mail с MD5 и URL файла запишите в email_data.txt через пробел почтовый адрес отправителя, пароль и параметры smtp-сервера.
Например, для mail.ru:
sender@mail.ru password smtp.mail.ru 465

Для запуска сервера выполните:
> python -m aiohttp_server.py

Сервер запустится по адресу localhost:8000


#### Работа с приложением

Поддерживаются POST-запросы для расчета MD5. Передается URL файла и e-mail пользователя (опционально). Если e-mail-указан, после завершения расчета на него придет результат. В ответ на POST-запрос пользователю возвращается id задачи. Пример запроса:
> curl -X POST -d "email=user@example.com&url=http://site.com/file.txt" http://localhost:8000/submit

{"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}

С помощью GET-запроса с идентификатором задачи можно узнать ее статус (задача выполняется, задача завершена, задачи не существует, задача завершилась неудачей).Пример запроса:
> curl -X GET http://localhost:8000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac

{"status":"running"}
