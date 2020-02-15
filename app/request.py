import urllib.request, json
from .models import Quote

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
            response = get_response
            results = process_results(response)

        return results


def process_results(result):
    quote_result = []

    for results in result:
        author = results.get('author')
        quote = results.get('quote')

        if quote:
            quote_instance = Quote(author, quote)
            quote_result.append(quote_instance)

    return quote_result
