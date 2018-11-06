import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # async defination
    # CELERY_BROKER_URL = 'sqla+mysql+mysqlconnector://test:test@127.0.0.1/mq'
    # CELERY_RESULT_BACKEND = 'db+mysql+mysqlconnector://test:test@127.0.0.1/mq'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # ZABBIX_URL = 'http://107.151.184.138:5002/api/v1.0/'
    # LINKMON_URL = 'http://107.151.184.138:5001/api/v1.0/'
    # # LINKMON_URL = 'http://localhost:5001/api/v1.0/'
    # AUTOROUTE_URL = 'http://128.14.52.114:5004/api/v1.0/'
    # ALERT_URL = 'http://107.151.184.138:5005/api/v1.0/'
    # SNMP_URL = 'http://107.151.184.138:5006/api/v1.0/'
    # #SNMP_URL = 'http://localhost:5006/api/v1.0/'
    # ECN_URL = 'http://107.151.184.138:5050/api/v1.0/'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://test:test@127.0.0.1/core_dev'
    # ALERT_WEB_SOCKET_URL = 'http://107.151.184.138:5005/'
    # ANSIBLE_URL = 'http://107.151.184.138:5002/api/v1.0/'

    DEBUG = True


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://test:test@127.0.0.1/core_prod'

    # ZABBIX_URL = 'http://control.zenlayer.net:5002/api/v1.0/'
    # LINKMON_URL = 'http://control.zenlayer.net:5001/api/v1.0/'
    # AUTOROUTE_URL = 'http://128.14.52.114:5004/api/v1.0/'
    # ALERT_URL = 'http://control.zenlayer.net:5005/api/v1.0/'
    # SNMP_URL = 'http://control.zenlayer.net:5006/api/v1.0/'
    # ECN_URL = 'http://control.zenlayer.net:5050/api/v1.0/'
    # ALERT_WEB_SOCKET_URL = 'http://control.zenlayer.net:5005/'
    # ANSIBLE_URL = 'http://control.zenlayer.net:5002/api/v1.0/'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
