import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from meritcs import update_data, get_remaining_days

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    # 不能注册全局的 不然会导致就算你数据采集不到他也会一直显示上次的数据
    REGISTRY = CollectorRegistry(auto_describe=False)
    domain_status = Gauge(
        "domain_status",
        "check the status of domains",
        ["domain", "issuer", "end_time"],
        registry=REGISTRY,
    )
    # 取得更新後info資訊
    domains_info = update_data()

    for domain_info in domains_info:
        Expiration_days_left = get_remaining_days(
            expiration_date=domain_info["End_time"]
        )
        domain_status.labels(
            domain=domain_info["Domain"],
            issuer=domain_info["Issuer"],
            end_time=domain_info["End_time"],
        ).set(Expiration_days_left)

    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


@app.route("/")
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9103, debug=True)