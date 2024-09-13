## Описание проекта.
Проект представляет собой DRF API для магазина продуктов. Этот сервис позволяет с помощью админ панели добавлять продукты, категории и подкатегории продуктов. Пользователь имеет возможность регистрации, добавления продуктов в корзину, изменения числа продуктов в корзине и удалении продуктов из корзины. 


## Стек технологий.

Python, Django, Django Rest Framework, Djoser.


## Установка и запуск.

1. Клонировать проект, создать и активировать виртуальное окружение, установить зависимости:

```
git clone git@github.com:monemonic/DRF-shop.git
cd DRF-shop
python3.9 -m venv venv
. venv/bin/activat
python3.9 -m pip install --upgrade pip
pip install -r requirements.txt

```

2. Перейти в папку /backend, применить миграции:

```
cd backend
python3.9 manage.py migrate
```

3. Создать суперпользователя и через админку заполнить БД (категории, подкатегории, продукты):

```
python3.9 manage.py createsuperuser
```

4. Запустить проект:

```
python3.9 manage.py runserver
```
## Примеры запросов и ответов на них:

1. POST запрос к /api/auth/users/ формата:

```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "password": "Qwerty123"
}
```
Зарегистрирует пользователя и вернет ответ формата:

```
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "id": 3
}
```

При незаполнении одного или нескольких обязательных полей будет получена ошибка с ответом формата:

```
{
  "field_name": [
    "Обязательное поле."
  ]
}
```
2. POST запрос к /api/auth/token/login/ формата:
```
{
  "username": "vasya.pupkin",
  "password": "Qwerty123"
}
```

Сформирует токен для указанного пользователя в формате:

```
{
    "auth_token": "eab45ccb7b5da3847abf68646084742342a9e995"
}
```

3. GET запрос к /api/categories/ вернет список всех имеющихся категорий с подкатегориями в формате:

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Овощи",
            "picture": "http://127.0.0.1:8000/media/backend/categories/categories.png",
            "subcategory": [
                {
                    "id": 1,
                    "category": 1,
                    "name": "Замороженные",
                    "picture": "/media/backend/categories/subcategory.jpg"
                },
                {
                    "id": 2,
                    "category": 1,
                    "name": "Утренний перекус",
                    "picture": "/media/backend/categories/subcategory.jpg"
                }
            ]
        }
    ]
}
```

4. GET запрос к /api/products/ вернет список всех имеющихся продуктов в формате:

```
{
    "count": 1,
    "next": "http://127.0.0.1:8000/api/products/?page=2",
    "previous": null,
    "results": [
        {
            "name": "Авокадо",
            "slug": "avocado",
            "subcategory": {
                "id": 1,
                "category": 1,
                "name": "Замороженные",
                "picture": "http://127.0.0.1:8000/media/backend/categories/subcategory.jpg"
            },
            "category": {
                "id": 1,
                "name": "Овощи",
                "picture": "/media/backend/categories/category.png"
            },
            "price": 200,
            "picture": [
                {
                    "image": "/media/backend/products/products1.jpg"
                },
                {
                    "image": "/media/backend/products/products2.png"
                },
                {
                    "image": "/media/backend/products/products2.png"
                }
            ]
        }
    ]
}
```

5. GET запрос к /api/products/{id}/ вернет продукт с указанным id в формате:

```
{
            "name": "Авокадо",
            "slug": "avocado",
            "subcategory": {
                "id": 1,
                "category": 1,
                "name": "Замороженные",
                "picture": "http://127.0.0.1:8000/media/backend/categories/subcategory.jpg"
            },
            "category": {
                "id": 1,
                "name": "Овощи",
                "picture": "/media/backend/categories/category.png"
            },
            "price": 200,
            "picture": [
                {
                    "image": "/media/backend/products/products1.jpg"
                },
                {
                    "image": "/media/backend/products/products2.png"
                },
                {
                    "image": "/media/backend/products/products2.png"
                }
            ]
        }
```

5. POST запрос к /api/products/{id}/add_shopping_cart/ вернет продукт с указанным id в формате:

```
{
    "product": {
        "name": "Авокадо",
        "slug": "avocado",
        "subcategory": {
            "id": 1,
            "category": 1,
            "name": "Замороженные",
            "picture": "/media/backend/categories/subcategory.jpg"
        },
        "category": {
            "id": 1,
            "name": "Овощи",
            "picture": "/media/backend/categories/category.png"
        },
        "price": 200,
        "picture": [
            {
                "image": "/media/backend/products/picture1.jpg"
            },
            {
                "image": "/media/backend/products/picture2.png"
            },
            {
                "image": "/media/backend/products/picture3.png"
            }
        ]
    },
    "amount": 1,
    "price": 200
}
```

5. PATCH запрос к /api/products/{id}/add_shopping_cart/ требует указания в запросе поля "amount" в формате числа, знаков "+" или "-".:

Запрос к указанному эндпроинту в данном формате увеличит значение "amount" у добавленного в корзину на 1:

```
{
    "amount": "+"
}
```

Запрос к указанному эндпроинту в данном формате уменьшит значение "amount" у добавленного в корзину на 1:

```
{
    "amount": "-"
}
```

Запрос к указанному эндпроинту в данном формате изменит значение "amount" на указанное в запросе, т.е. "amount" станет равным 10:

```
{
    "amount": 10
}
```

В случае, если такой запрос отправляется к продукту, который не добавлен в корзину, будет возвращена ошибка 404:

```
{
    "detail": "No ShoppingCart matches the given query."
}
```

6. DELETE запрос к /api/products/{id}/add_shopping_cart/ удалит из корзины указанный продукт и вернет следующий ответ:

```
"Продукт успешно удален из корзины"
```

В случае, если продукт не был добавлен в корзину, запрос вернет ответ ответ следующего формата:

```
"Вы не добавляли в корзину этот продукт."
```

7. DELETE запрос к /api/products/clean_all_shopping_cart/ удалит из корзины все добавленные продукты и вернет следующий ответ:

```
"Корзина успешно очищена."
```

8. GET запрос к /api/products/shopping_cart/ вернет ответ содержащий все добавленные в корзину продукты, с указанием количества продуктов и их общей стоимости, формата:

```
{
    "products": [
        {
            "product": {
                "name": "Авокадо",
                "slug": "avocado",
                "subcategory": {
                    "id": 1,
                    "category": 1,
                    "name": "Замороженные",
                    "picture": "/media/backend/categories/subcategory.jpg"
                },
                "category": {
                    "id": 1,
                    "name": "Овощи",
                    "picture": "/media/backend/categories/category.png"
                },
                "price": 200,
                "picture": [
                    {
                        "image": "/media/backend/products/picture1.jpg"
                    },
                    {
                        "image": "/media/backend/products/picture2.png"
                    },
                    {
                        "image": "/media/backend/products/picture3.png"
                    }
                ]
            },
            "amount": 1,
            "price": 200
        },
        {
            "product": {
                "name": "Апельсин",
                "slug": "apelsin",
                "subcategory": {
                    "id": 1,
                    "category": 1,
                    "name": "Замороженные",
                    "picture": "/media/backend/categories/subcategory.jpg"
                },
                "category": {
                    "id": 1,
                    "name": "Овощи",
                    "picture": "/media/backend/categories/category.png"
                },
                "price": 1212,
                "picture": [
                    {
                        "image": "/media/backend/products/picture1.jpg"
                    },
                    {
                        "image": "/media/backend/products/picture2.png"
                    },
                    {
                        "image": "/media/backend/products/picture3.png"
                    }
                ]
            },
            "amount": 1,
            "price": 1212
        }
    ],
    "total_price": 1412,
    "count": 2
}
```