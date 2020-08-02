# /start_bot.py file
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import logging
import time

from flask import Flask, request
import flask
import telebot
import selenium
from selenium import webdriver

from config import API_TOKEN, \
    WEBHOOK_HOST, \
    WEBHOOK_PORT, \
    WEBHOOK_LISTEN, \
    WEBHOOK_SSL_CERT, \
    WEBHOOK_SSL_PRIV, \
    WEBDRIVER_NAME

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def command_start_handler(message):
    cid = message.chat.id
    bot.send_message(cid, 'The bot makes web page screenshot by given url and send it to you. '
                          'Enter url for which you want screenshot')


# Handle url
@bot.message_handler(func=lambda m: True)
def make_page_shot(message):
    cid = message.chat.id
    url = message.text
    logger.debug(f"process url {url}")
    try:
        driver = webdriver.Chrome(WEBDRIVER_NAME)
        try:
            driver.get(url)
            screenshot = driver.get_screenshot_as_png()
            input = io.BytesIO(screenshot)
            bot.send_photo(cid, input)
        except selenium.common.exceptions.InvalidArgumentException as e:
            bot.send_message(cid, f'Bad input string "{url}". Error message: {e} ')
        finally:
            if driver:
                driver.quit()
    except Exception as e:
        bot.send_message(cid, f'Error message {e}')


# Process webhook calls
@server.route(WEBHOOK_URL_PATH, methods=['POST'])
def process_webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        logger.debug(f"webhook calls {json_string}")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


bot.remove_webhook()
time.sleep(1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
server.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)