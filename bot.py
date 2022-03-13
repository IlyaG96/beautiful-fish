import redis
from environs import Env
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)
from enum import Enum
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from elastic_api import get_client_token, fetch_products


class BotStates(Enum):
    ASK_QUESTION = 1
    CHECK_ANSWER = 2
    USER_CHOSE_ACTION = 3


def start(update, context):
    client_id = context.bot_data['client_id']
    client_secret = context.bot_data['client_secret']
    elastic_token = get_client_token(client_secret, client_id)
    products = fetch_products(elastic_token)

    keyboard = [[
        InlineKeyboardButton(product.get('name'), callback_data=num) for num, product in enumerate(products)
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Мы рыбов продоем!', reply_markup=reply_markup)

    return BotStates.ASK_QUESTION


def cancel(update, context):
    text = 'Пока'

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def button(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


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
            BotStates.ASK_QUESTION: [
                CallbackQueryHandler(button),
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
