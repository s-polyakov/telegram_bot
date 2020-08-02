# Telegram bot

## Takes screenshot of the given url
## Instalation

- **Install Python packages**

pip install -r requirements.txt

- **Download appropriate webdriver for selenium**

- **Create ssl certificate:**

Quick and dirty SSL certificate generation:

openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
with the same value in you put in WEBHOOK_HOST 

- **Create file config.py from confif_example.py and fill it:**

API_TOKEN = \<telegramm token>

WEBHOOK_HOST = \<url or ip of the bot server>

WEBHOOK_PORT = \<port>  # 443, 80, 88 or 8443 (port need to be 'open')

WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate

WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBDRIVER_NAME = 'chromedriver'
