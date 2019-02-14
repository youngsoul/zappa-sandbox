import requests
import json

aws_url = 'https://449re21ky1.execute-api.us-east-1.amazonaws.com/flask_microservice'


def add_user(email, username, password):
    route_url = '/flask_microservice/user'
    payload = {
        'username': username,
        'password': password,
        'emailaddress': email
    }

    response = requests.post(url=f'{aws_url}{route_url}', json=payload)
    print(response)

def get_user(email):
    route_url = f'/flask_microservice/user/{email}'
    response = requests.get(url=f'{aws_url}{route_url}')
    print(response.content)


if __name__ == '__main__':
    add_user('foo@bar.com', 'foo', 'bar')
    get_user('foo@bar.com')
