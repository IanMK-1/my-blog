from flask import render_template
from ..request import obtain_quote
from . import main


@main.route('/')
def index():
    quote = obtain_quote()

    return render_template('index.html', quote=quote)


@main.route('/blogs')
def blogs():
    return render_template('blogs.html')
