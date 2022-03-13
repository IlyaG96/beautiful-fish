import redis
from environs import Env
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)
from enum import Enum
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from elastic_api import get_client_token, fetch_products, get_product_info
from textwrap import dedent


class BotStates(Enum):
    START = 1
    HANDLE_MENU = 2
    USER_CHOSE_ACTION = 3


def format_product_description(product_description):
    product_description = product_description.get('data')
    print(product_description)

    formatted_product_description = dedent(
        f'''
        Название : {product_description['name']}
        Цена : {product_description['meta']['display_price']['with_tax']['formatted']} usd/кг
        На складе : {product_description['meta']['stock']['level']} кг
        Описание : {product_description['description']}
        '''
    )

    return formatted_product_description


def start(update, context):
    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    elastic_token = get_client_token(client_secret, client_id)
    products = fetch_products(elastic_token)
    context.bot_data['products'] = products
    bot = context.bot

    keyboard = [[
        InlineKeyboardButton(product.get('name'), callback_data=product.get('id')) for product in products
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(text='Мы рыбов продоем!',
                     chat_id=update.message.chat_id,
                     reply_markup=reply_markup)

    return BotStates.HANDLE_MENU


def cancel(update, context):
    text = 'Пока'

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def handle_menu(update, context):

    products = context.bot_data['products']
    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    bot = context.bot

    elastic_token = get_client_token(client_secret, client_id)

    callback_query = update.callback_query
    product_id = callback_query.data
    product_description = get_product_info(elastic_token, product_id)
    formatted_product_description = format_product_description(product_description)

    keyboard = [[
        InlineKeyboardButton(product.get('name'), callback_data=product.get('id')) for product in products
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(text=formatted_product_description,
                          chat_id=callback_query.message.chat_id,
                          message_id=callback_query.message.message_id,
                          reply_markup=reply_markup)

    return BotStates.HANDLE_MENU


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

    start_quiz = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('cancel', cancel)
        ],
        states={
            BotStates.START: [
                CallbackQueryHandler(start)
            ],
            BotStates.HANDLE_MENU: [
                CallbackQueryHandler(handle_menu),
            ],

        },

        per_user=True,
        per_chat=True,
        fallbacks=[
            CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(start_quiz)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
