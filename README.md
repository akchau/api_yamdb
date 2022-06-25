# api_yamdb
api_yamdb

### Описание эндпоинтов:

##### Авторизация:

`[POST]: http://127.0.0.1:8000/api/v1/auth/signup/` - Получить код подтверждения на переданный email. Регистрация пользователя
`ДОСТУП/:Доступно любому пользователю.`
```JSON
{
  "email": "string",
  "username": "string"
}
```
Поля `email`, `username` - уникальные. `username` не может быть `me`

`[POST]: http://127.0.0.1:8000/api/v1/auth/token/` - Получить токен. В обмен на код подтверждения который пришел на почту и логин.
`ДОСТУП/:Доступно любому пользователю.`
```JSON
{
  "username": "string",
  "confirmation_code": "string"
}
```


##### Пользовательское управление

`[GET]: http://127.0.0.1:8000/api/v1/users/me/` - Получить информацию о своей странице.
`ДОСТУП/:Доступно авторизованному пользователю.`

`[PATCH]: http://127.0.0.1:8000/api/v1/users/me/` - Изменить свои данные.
`ДОСТУП/:Доступно авторизованному пользователю.`
```JSON
{
    "username" : "update_user",
    "first_name": "Update", 
    "last_name": "Update",
    "bio": "Born. Update",
    "role": "user"
}
```


##### Администрирование

`[GET]: http://127.0.0.1:8000/api/v1/users/` - Получить список всех пользовтателей.
`ДОСТУП/:Доступно только администратору.`

`[POST]: http://127.0.0.1:8000/api/v1/users/` - Добавить пользователя. Если данные валидны, будет создан новый пользователь.
`ДОСТУП/:Доступно только администратору.`
```JSON
{
    "username" : "new_user",
    "email": "new_user@test.te.",
    "first_name": "New", 
    "last_name": "User",
    "bio": "Born.",
    "role": "user"
}
```

`[GET]: http://127.0.0.1:8000/api/v1/new_user/` - Получить пользователя с `username="new_user"`
`ДОСТУП/:Доступно только администратору.`

`[PUT]: http://127.0.0.1:8000/api/v1/new_user/` - Заменить пользователя с `username="new_user"`
`ДОСТУП/:Доступно только администратору.`
```JSON
{
    "username" : "put_user",
    "email": "put_user@test.te.",
    "first_name": "Put", 
    "last_name": "User",
    "bio": "Born.Put.",
    "role": "user"
}
```

`[PATCH]: http://127.0.0.1:8000/api/v1/new_user/` - Частично изменить пользователя с `username="new_user"`
`ДОСТУП/:Доступно только администратору.`
```JSON
{
    "username" : "put_user",
    "first_name": "Put", 
    "bio": "Born.Put.",
    "role": "user"
}
```

`[DELETE]: http://127.0.0.1:8000/api/v1/new_user/` - Удалить пользователя с `username="new_user"`
`ДОСТУП/:Доступно только администратору.`

# Для загрузка данных получаемых вместе с проектом 
```
python3 manage.py dbload 

```

Супер проект Андеря, Глеба, Димы
