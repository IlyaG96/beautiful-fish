import requests


def fetch_products(elastic_token):

    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    response.raise_for_status()

    products = response.json().get('data')

    return products


def get_product_info(elastic_token, product_id):

    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/products/{product_id}', headers=headers)
    response.raise_for_status()

    return response.json()


def get_image_link(elastic_token, product_image_id):

    headers = {
        f'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/files/{product_image_id}', headers=headers)
    response.raise_for_status()
    image_link = response.json()['data']['link']['href']

    return image_link


def get_client_auth(client_secret, client_id):

    data = {
        f'client_id': {client_id},
        f'client_secret': {client_secret},
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()

    return response.json()


def add_product_to_cart(elastic_token, cart_id, product_id, quantity):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        },
    }

    response = requests.post(f'https://api.moltin.com/v2/carts/{cart_id}/items', headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()


def remove_product_from_cart(elastic_token, cart_id, product_id):

    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }
    response = requests.delete(f'https://api.moltin.com/v2/carts/{cart_id}/items/{product_id}', headers=headers)
    response.raise_for_status()

    return response.json()


def create_cart(elastic_token, tg_id):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }
    json_data = {
        'data': {
            'name': tg_id,
            'description': f'cart of user {tg_id}',
        }
    }
    response = requests.post('https://api.moltin.com/v2/carts', headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()


def get_cart(elastic_token, cart_id):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/carts/{cart_id}/items', headers=headers)
    response.raise_for_status()

    return response.json()


def get_cart_total_price(elastic_token, cart_id):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/carts/{cart_id}', headers=headers)
    response.raise_for_status()

    return response.json()


def create_customer(elastic_token, user_id, email):

    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    json_data = {
        'data': {
            'type': 'customer',
            'name': f'{user_id}',
            'email': f'{email}',
            'password': 'mysecretpassword',
        },
    }

    response = requests.post('https://api.moltin.com/v2/customers', headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()


def check_customer(elastic_token, client_id):

    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/customers/{client_id}', headers=headers)
    response.raise_for_status()

    return response.json()

