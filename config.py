class Config:
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    Debug = True
