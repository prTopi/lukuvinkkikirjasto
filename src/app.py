from flask import Flask

app = Flask(__name__)


@app.route('/health')
def health():
    return "Health check: ✅"


@app.route('/')
def index():
    return "Lukuvinkkikirjasto"
