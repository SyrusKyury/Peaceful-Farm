import requests
json = {
    "api_key": "1234567890",
    "flags": [
        "string",
        "test1",
        "test2",
        "test3"
    ],
    "exploit": "string",
    "service": "string",
    "nickname": "string"
}

post = requests.post('http://localhost/flags', json=json)
print(post.text)