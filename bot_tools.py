from textwrap import dedent


def format_product_description(product_description):
    product_description = product_description['data']

    formatted_product_description = dedent(
        f'''
        Название : {product_description['name']}
        Цена : {product_description['meta']['display_price']['with_tax']['formatted']} usd/кг
        На складе : {product_description['meta']['stock']['level']} кг
        Описание : {product_description['description']}
        '''
    )

    return formatted_product_description


def format_cart(cart_items, total_price):
    cart = cart_items['data']
    formatted_cart = ''
    for item in cart:
        product = item['name']
        quantity = item['quantity']
        price = item['meta']['display_price']['without_tax']['value']['formatted']
        description = item['description']
        formatted_cart += dedent(
            f'''
        Товар {product} 
        {description}
        
        В количестве: {quantity} шт
        На сумму: {price}

        ''')

    return dedent(
        f'''
    {formatted_cart}
    Общая сумма: {total_price}
    ''')
