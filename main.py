from environs import Env
import requests
from pprint import pprint


def show_cart(elastic_token):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
    }

    response = requests.get('https://api.moltin.com/v2/carts/abc', headers=headers)
    pprint(response.json())


def add_to_cart(elastic_token,
                product_type,
                product_name,
                product_sku,
                product_description,
                quantity,
                price):
    headers = {
        'Authorization': f'Bearer {elastic_token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'data': {
            'type': f'{product_type}',
            'name': f'{product_name}',
            'sku': f'{product_sku}',
            'description': f'{product_description}',
            'quantity': quantity,
            'price': {
                'amount': price,
            },
        },
    }

    response = requests.post('https://api.moltin.com/v2/carts/abc/items', headers=headers, json=json_data)
    print(response.json())


def main():
    env = Env()
    env.read_env()
    elastic_token = env.str('ELASTIC_TOKEN')

    add_to_cart(elastic_token,
                'custom_item',
                'blue fish',
                'fish-02',
                'gorgeous blue fish',
                1,
                20000)

    show_cart(elastic_token)


if __name__ == '__main__':
    main()