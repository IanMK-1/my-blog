import urllib.request, json
from .models import Quote

quotes_url = None


def configure_request(app):
    global quotes_url
    quotes_url = app.config['QUOTES_URL']
