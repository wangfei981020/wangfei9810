import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from metrics import Metrics

app = Flask(__name__)

# REGISTRY = CollectorRegistry(auto_describe=False)

# online_status = Gauge(
#     "online_players_status",
#     "check the online players",
#     ["project", "vid", "gmtype"],
#     registry=REGISTRY,
# )


@app.route("/metrics")
def metrics():
    REGISTRY = CollectorRegistry(auto_describe=False)
    online_status = Gauge(
        "online_players_status",
        "check the online players",
        ["project", "vid", "gmtype"],
        registry=REGISTRY,
    )

    data = Metrics().run()
    for p in data:
        for v in p:
            online_status.labels(
                project=v["project"],
                vid=v["vid"],
                gmtype=v["gmtype"],
            ).set(v["players"])

    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


@app.route("/")
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9102, debug=True)
