# CollectionDrive-Back-end-

documentation

------------authorization----------
[domain_name]/auth/token/ -- accepts 2 parameters username and password 
POST [domain_name]/auth/token/
{
    'username':'...',
    'passwrod':'...'
}

response is JWT access token
{
    "refresh": "...",
    "access": "..."
}

then you have to use this token for different requests
token lifetime -- 120 minutes, after token expires, make POST request to 

----social auth-----
POST [domain_name]/auth/google/
or
POST [domain_name]/auth/facebook/
{
    'token':'token taken in front side'
}

response is JWT access token
{
    "refresh": "...",
    "access": "..."
}

for example to take token you can use  https://www.facebook.com/v6.0/dialog/oauth?client_id=2500936673496401&response_type=token&redirect_uri=http://localhost:4200/
such url

[domain_name]/auth/token/refresh/ 
POST 
{
    'username':'...',
    'passwrod':'...'
}
response is JWT access token
{
    "refresh": "...",
    "access": "..."
}

but this JWT token lifetime is longer (1 day)

--------registration--------
make POST request to [domani_name]/auth/users/ with username, password, email, and lang(default is 'en')

POST [domain_name]/auth/users/
{
    'username':'...',
    'password':'...',
    'email':'...',
    'lang':'en'
}

lang can be 'en' or 'ru'

the Response will be 

{
    "id": ...,
    "username": "...",
    "email": "...",
    "lang": "..."
}

with codes 201__created or 400__bad_request

----------get list of all users------
GET [domain_name]/auth/users/
example of response:
[
    {
        "id": 1,
        "username": "remmidemmi",
        "email": "popelnyk@icloud.com",
        "lang": "en",
        "total_collections": 1,
        "collections": [
            {
                "id": 2,
                "name": "vino",
                "description": "lol"
            }
        ]
    },
    {
        "id": 2,
        "username": "chocoretgnchioenrgci",
        "email": "alexy-lex212@yndex.ru",
        "lang": "en",
        "total_collections": 0,
        "collections": []
    }
]

----get list of collections----
GET [domain_name]/main/collections/
exmaple of response
[
    {
        "id": 2,
        "owner": "remmidemmi",
        "owner_id": 1,
        "name": "vino",
        "theme_name": "alkohol2",
        "description": "lol",
        "creation_date": "2020-04-03T19:48:51.519463Z",
        "item_text_fields": [
            "taste",
            "comment"
        ],
        "item_int_fields": [
            "cost"
        ],
        "item_bool_fields": [
            "expensive?"
        ],
        "item_date_fields": [
            "bought"
        ],
        "total_of_items": 1,
        "items": [
            {
                "id": 31,
                "name": "vino241343",
                "collection_id": 2,
                "fields": {
                    "taste": "good",
                    "comment": "cool",
                    "cost": 4,
                    "expensive?": 0,
                    "bought": "2020-01-2"
                }
            }
        ]
    }
]

------get best collections (max 10)-----
GET [domain_name]/main/collections/best/
example of response:
[
    {
        "id": 3,
        "name": "vino",
        "theme": "alkohol2",
        "description": "lol",
        "creation_date": "2020-04-04T03:26:22.764055Z",
        "total_of_items": 3
    },
    {
        "id": 2,
        "name": "vino",
        "theme": "alkohol2",
        "description": "lol",
        "creation_date": "2020-04-03T19:48:51.519463Z",
        "total_of_items": 1
    },
    {
        "id": 4,
        "name": "vino",
        "theme": "alkohol2",
        "description": "lol",
        "creation_date": "2020-04-04T03:26:31.642384Z",
        "total_of_items": 0
    }
]

---create collection----
HEADERS MUST INCLUDE JWT TOKEN "Authorization": "Bearer <token>"
POST [domain_name]/main/collections/
example of request:
{
    'name':'...',
    'description':'...',
    'theme_name':'...',
    'item_text_fields':
            [
                "taste",
                "comment"
            ],
    'item_int_fields':
            [
                "cost"
            ],
    'item_bool_fields':
            [
                "expensive?"
            ],
    'item_date_fields':
            [
                "when i bought it"
            ],
}

-----add item------
HEADERS MUST INCLUDE JWT TOKEN "Authorization": "Bearer <token>"
POST [domain_name]/main/collections/{id}/create_item/

{
    'name':'...',
    'fields':
        {
            "taste":"good",
            "comment":"cool",
            "cost":4,
            "expensive?":1,
            "bought":"2020-01-24"
        },
    'tags':
        [
            {'name':'...'}, 
            {'name':'...'}, 
            {'name':'...'}
        ]
}

----delete item-----
HEADERS MUST INCLUDE JWT TOKEN "Authorization": "Bearer <token>"
DELETE [domain_name]/main/items/{id}/
 
----delete collection----
HEADERS MUST INCLUDE JWT TOKEN "Authorization": "Bearer <token>"
DELETE [domain_name]/main/collection/{id}/




