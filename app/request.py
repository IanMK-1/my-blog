import urllib.request, json

quotes_url = None


def configure_request(app):
    global quotes_url
    quotes_url = app.config['QUOTES_URL']


def obtain_quote():
    """Obtains the quotes from the url"""

    with urllib.request.urlopen(quotes_url) as source_url:
        get_quote = source_url.read()
        get_response = json.loads(get_quote)

        results = None

        if get_response:
            results = get_response

        return results

