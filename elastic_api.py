import requests
from environs import Env


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


def get_client_token(client_secret, client_id):

    data = {
        f'client_id': {client_id},
        f'client_secret': {client_secret},
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()

    return response.json().get('access_token')


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

def main():

    env = Env()
    env.read_env()
    client_id = env.str('ELASTIC_CLIENT_ID')
    client_secret = env.str('ELASTIC_CLIENT_SECRET')
    elastic_token = get_client_token(client_secret, client_id)
    fetch_products(elastic_token)
    #cart_id = create_cart(elastic_token, tg_id='123').get('data').get('id')
    #current_cart = 'f2f86d7d-6a64-420e-b028-790fb39457e3'
    #get_cart(elastic_token, cart_id=current_cart)
    #add_product_to_cart(elastic_token, cart_id=current_cart, product_id='f200aec5-511f-409a-960d-be9195869436')
    #get_cart(elastic_token, cart_id=current_cart)


if __name__ == '__main__':
    main()
