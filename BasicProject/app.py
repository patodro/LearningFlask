"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# URL: /hello/<name>?message=I%20love%20Josh%20Allen
@app.route('/')
@app.route('/hello/<name>')
def hello(name):
    """Renders a sample page."""
    msg = request.args.get('message','')
    return "Hello "+ name + "! " + msg + "."

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
