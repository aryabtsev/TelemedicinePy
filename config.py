token = '290824130:AAGjbVy6uGN_lb_DZGRe0hZDxHqvndRJV6U'
database_name = 'DataBaseTest.db'


WEBHOOK_HOST = '173.230.151.37'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '../webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '../webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)