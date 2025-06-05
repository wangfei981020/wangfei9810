import logging
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from metrics import GameDataProcessor

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route("/metrics")
def metrics():
    REGISTRY = CollectorRegistry(auto_describe=False)
    online_status = Gauge(
        "online_players_status",
        "check the online players",
        ["project", "vid", "gmtype"],
        registry=REGISTRY,
    )

    processor = GameDataProcessor()
    data = processor.run()
    for v in data:
        logger.info(f"Processed data: {v}")
        players = v["players"]
        online_status.labels(
            project=v["project"],
            vid=v["vid"],
            gmtype=v["gmtype"],
        ).set(players)
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


@app.route("/")
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9102, debug=True)

