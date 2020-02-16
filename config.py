import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ian:ian@localhost/blog'
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'production': ProdConfig,
    'development': DevConfig
}
