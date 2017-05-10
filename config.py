import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # Mysql config
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'sale_db'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_CHARSET = 'utf8'

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Redis config
    REDIS_URL = "redis://:fromtrain!QAZ@101.200.38.103:6379/0"

    # Log config
    LOGCONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stderr'
            },
            'info_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': 'log/info.log',
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 3,
                'encoding': 'utf8'
            },
            'debug_file_handler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'filename': 'log/debug.log',
                'when': 'D',
                'interval': 1,
                'backupCount': 10,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            'ticketServer': {
                'handlers': ['info_file_handler'],
                'level': 'DEBUG'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file_handler']
        }

    }





config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}