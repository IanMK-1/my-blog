class Config:
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'production': ProdConfig,
    'development': DevConfig
}
