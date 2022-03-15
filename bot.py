import redis
from environs import Env
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from enum import Enum
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from elastic_api import get_client_token, fetch_products, get_product_info, \
    get_image_link, get_cart, add_product_to_cart, create_cart
from textwrap import dedent


class BotStates(Enum):
    START = 1
    HANDLE_MENU = 2
    HANDLE_DESCRIPTION = 3


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

def format_basket(basket_content):
    pass


def cancel(update, context):
    text = 'Пока'

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def handle_menu(update, context):
    if not update.callback_query:
        user_id = update.message.chat_id
    else:
        user_id = update.callback_query.message.chat_id
    context.bot_data['user_id'] = user_id
    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    elastic_token = get_client_token(client_secret, client_id)
    products = fetch_products(elastic_token)
    context.bot_data['products'] = products
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton(product.get('name'), callback_data=product.get('id')) for product in products],
        [InlineKeyboardButton('Корзина', callback_data='Корзина')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(text='Мы рыбов продоем!',
                     chat_id=user_id,
                     reply_markup=reply_markup)

    return BotStates.HANDLE_DESCRIPTION


def handle_description(update, context):
    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    bot = context.bot

    elastic_token = get_client_token(client_secret, client_id)

    callback_query = update.callback_query
    product_id = callback_query.data
    context.bot_data['product_id'] = product_id

    product_description = get_product_info(elastic_token, product_id)
    product_image_id = product_description['data']['relationships']['main_image']['data']['id']
    image_link = get_image_link(elastic_token, product_image_id)
    formatted_product_description = format_product_description(product_description)

    keyboard = [[
        InlineKeyboardButton('Назад', callback_data='Назад'),
        InlineKeyboardButton('1 кг', callback_data='1'),
        InlineKeyboardButton('5 кг', callback_data='5'),
        InlineKeyboardButton('10 кг', callback_data='10'),
        InlineKeyboardButton('Корзина', callback_data='Корзина')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_photo(
        chat_id=callback_query.message.chat_id,
        photo=image_link,
        caption=formatted_product_description,
        reply_markup=reply_markup
    )

    bot.delete_message(
        chat_id=callback_query.message.chat_id,
        message_id=callback_query.message.message_id,
    )

    return BotStates.HANDLE_DESCRIPTION


def update_basket(update, context):

    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    elastic_token = get_client_token(client_secret, client_id)
    user_id = str(context.bot_data['user_id'])
    cart_id = context.bot_data.get('cart_id')
    product_id = context.bot_data['product_id']

    if not cart_id:
        cart_id = create_cart(elastic_token, user_id)['data']['id']
        context.bot_data['cart_id'] = cart_id

    callback_query = update.callback_query
    quantity = int(callback_query.data)

    add_product_to_cart(elastic_token, cart_id, product_id, quantity)
    get_cart(elastic_token, cart_id)

    return BotStates.HANDLE_DESCRIPTION


def handle_basket(update, context):

    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    products = context.bot_data['products']
    elastic_token = get_client_token(client_secret, client_id)
    cart_id = context.bot_data.get('cart_id')
    callback_query = update.callback_query
    bot = context.bot
    cart = get_cart(elastic_token, cart_id)

    keyboard = [
        [InlineKeyboardButton(product.get('name'), callback_data=product.get('id')) for product in products],
        [InlineKeyboardButton('Корзина', callback_data='Корзина')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        text=cart,
        chat_id=callback_query.message.chat_id,
        reply_markup=reply_markup,
    )


def main():
    env = Env()
    env.read_env()
    telegram_token = env.str('TG_TOKEN')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_password = env.str('REDIS_PASSWORD')
    client_id = env.str('ELASTIC_CLIENT_ID')
    client_secret = env.str('ELASTIC_CLIENT_SECRET')

    updater = Updater(telegram_token)

    redis_base = redis.Redis(host=redis_host,
                             port=redis_port,
                             password=redis_password,
                             decode_responses=True)

    dispatcher = updater.dispatcher
    dispatcher.bot_data['redis_base'] = redis_base
    dispatcher.bot_data['client_id'] = client_id
    dispatcher.bot_data['client_secret'] = client_secret

    fish_shop = ConversationHandler(
        entry_points=[
            CommandHandler('start', handle_menu),
            CommandHandler('cancel', cancel)
        ],
        states={
            BotStates.HANDLE_MENU: [
                CallbackQueryHandler(handle_menu),
                CallbackQueryHandler(handle_basket, pattern='^Корзина'),
            ],
            BotStates.HANDLE_DESCRIPTION: [
                CallbackQueryHandler(handle_menu, pattern='^Назад$'),
                CallbackQueryHandler(handle_basket, pattern='^Корзина'),
                CallbackQueryHandler(update_basket, pattern='^[0-9]+$'),
                CallbackQueryHandler(handle_description),
            ],

        },

        per_user=True,
        per_chat=True,
        fallbacks=[
            CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(fish_shop)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
