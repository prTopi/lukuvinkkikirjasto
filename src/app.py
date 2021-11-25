from flask import Flask

app = Flask(__name__)

import routes

@app.route('/health')
def health():
    return "Health check: ✅"

