#!/usr/bin/python3
"""
A simple Flask web application with multiple routes.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display 'Hello HBNB!'

    Returns:
        str: The message 'Hello HBNB!'
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display 'HBNB'

    Returns:
        str: The message 'HBNB'
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Display 'C ' followed by the value of the text variable

    Args:
        text (str): The text to display

    Returns:
        str: The message 'C ' followed by the value of the text variable
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """
    Display 'Python ' followed by the value of the text variable

    Args:
        text (str): The text to display (default is 'is cool')

    Returns:
        str: The message 'Python ' followed by the value of the text variable
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Display 'n is a number' only if n is an integer

    Args:
        n (int): The number to display

    Returns:
        str: The message 'n is a number' if n is an integer
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Display a HTML page only if n is an integer

    Args:
        n (int): The number to display

    Returns:
        rendered_template: HTML template displaying the number
    """
    return render_template('number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
