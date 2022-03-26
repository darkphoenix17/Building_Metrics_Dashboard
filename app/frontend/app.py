from flask import Flask, render_template, request
from flask_cors import CORS

from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)

metrics = GunicornInternalPrometheusMetrics(app)

CORS(app)

@app.route("/")
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
