import requests
from environs import Env


def fetch_products(elastic_token):
    import requests

    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    print(response.json())


def get_client_token(client_secret, client_id):

    data = {
        f'client_id': {client_id},
        f'client_secret': {client_secret},
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()

    return response.json().get('access_token')


def add_product_to_inventory(product_id, elastic_token):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }

    data = '{"data": {"quantity": 1000}}'

    response = requests.post(f'https://api.moltin.com/v2/inventories/{product_id}', headers=headers, data=data)


def get_inventory(elastic_token):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get('https://api.moltin.com/v2/inventories', headers=headers)
    print(response.json())


def get_product_stock(elastic_token, product_id):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/inventories/b8b38976-d669-49d9-9944-adae21b16a8a', headers=headers)
    print(response.json())


def create_product(elastic_token):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'type': 'product',
            'name': 'blue fish',
            'slug': 'blue-fish',
            'sku': 'blue-fish-001',
            'description': 'simple blue fish',
            'manage_stock': True,
            'price': [
                {
                    'amount': 3000,
                    'currency': 'USD',
                    'includes_tax': True,
                },
            ],
            'status': 'live',
            'commodity_type': 'physical',
        },
    }

    response = requests.post('https://api.moltin.com/v2/products', headers=headers, json=json_data)

    print(response.json())


def main():

    env = Env()
    env.read_env()
    client_id = env.str('ELASTIC_CLIENT_ID')
    client_secret = env.str('ELASTIC_CLIENT_SECRET')
    elastic_token = get_client_token(client_secret, client_id)
    fetch_products(elastic_token)


if __name__ == '__main__':
    main()
