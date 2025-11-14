from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Get the current directory (project root) to serve client files
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    """Serve the main chat client HTML page."""
    return send_from_directory(ROOT_DIR, 'client.html')


@app.route('/client.js')
def client_js():
    """Serve the client JavaScript file."""
    return send_from_directory(ROOT_DIR, 'client.js')


def run_web_server(host: str = '0.0.0.0', port: int = 5000):
    """Start the Flask web server."""
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    run_web_server()