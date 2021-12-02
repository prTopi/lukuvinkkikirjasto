"""Starts Flask server and populates routes"""
from flask import Flask

app = Flask(__name__)

# pylint: disable=C0413,W0611
import routes

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/health")
def health():
    return "Health check: ✅"
