"""Application exporter"""

from os import getenv
from prometheus_client import start_http_server, CollectorRegistry
import logging
from app_metrics import AppMetrics


def main():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    # Get config from env
    scrap_interval_seconds = int(getenv("SCRAP_INTERVAL_SECONDS", "60"))
    exporter_port = int(getenv("EXPORTER_PORT", "9000"))
    yaml_config_path = str(getenv("YAML_CONFIG_PATH", "config.yml"))
    # Log config
    logging.info(f"SCRAP_INTERVAL_SECONDS={scrap_interval_seconds}")
    logging.info(f"EXPORTER_PORT={exporter_port}")
    logging.info(f"YAML_CONFIG_PATH={yaml_config_path}")

    prom_registry = CollectorRegistry()
    app_metrics = AppMetrics(
        scrap_interval_seconds=scrap_interval_seconds,
        yaml_config_path=yaml_config_path,
        registry=prom_registry
    )
    start_http_server(exporter_port, registry=prom_registry)
    app_metrics.run_metrics_loop()


if __name__ == "__main__":
    main()
