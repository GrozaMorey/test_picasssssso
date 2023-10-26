Стек: Django, DRF, Celery, Postgresql, Redis, Gunicorn, Nginx
------------------------------------------------------
Connect
------------------------------------------------------
Эндпойнты доступны по адрсесу: 83.222.11.20/api/v1/


Endpoints
------------------------------------------------------

***upload/*** - Принимает только POST запросы требует вместе 
с запросом body по формату
```json
{
  "file": "form_file"
}
```

Пример:
```curl
curl --location --request POST '83.222.11.20/api/v1/upload/' --form 'file=@"/C:/Users/user/Downloads/test.jpeg"'
```

Затем запускает celery task в зависимости от расширения

***files/*** - Принимает только GET запросы и возвращает список
всех загруженных файлов


HighLoad
------------------------------------------------------


При ожидании высокой загрузки были бы применены следующие пункты:

- Переезд с Gunicorn на Bjoern так как он на поддерживает на порядок больше соединений

- Создание реплик приложений и кластеризация баз данных для балансировки нагрузки между ними

- Перенос хранение файлов на единное object storage в облаке по типу s3

- Деплой всех реплик на несколько серверов и настройка балансировщика нагрузки между ними

- Использовать kubernetes для оркестрации 


 
