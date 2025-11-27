import logging
from time import sleep

from prometheus_client import Gauge

from exporter_config import ExporterConfig
from utils import open_yaml


class AppMetrics:
    def dump_conf(self):
        for service, config in self.exporter_configs.items():
            self.logging.info(f"service: {service}")
            config.dump_conf(prefix="\t")

    def __init__(self, yaml_config_path, scrap_interval_seconds, registry):
        self.logging = logging.getLogger(__name__)
        self.logging.info("Prometheus exporter started")

        self.yaml_file = open_yaml(yaml_config_path)

        # Extra labels
        self.extra_labels_default = self.get_extra_labels()
        label_list = list(self.extra_labels_default.keys())
        label_list.append("service")

        # Configuration
        self.exporter_configs = self.parse_yaml_config()
        self.registry = registry
        self.scrap_interval_seconds = scrap_interval_seconds

        # Logging
        self.dump_conf()

        # Metrics file_stat_count
        self.file_stat_count = Gauge(
            name="file_stat_count",
            documentation="File count for the service",
            labelnames=label_list,
            registry=registry,
        )
        self.file_stat_last_modification_time = Gauge(
            name="file_stat_last_modification_time",
            documentation="Unix timestamp corresponding to the last "
            "file modification for the service",
            labelnames=label_list,
            registry=registry,
        )

        self.file_stat_last_file_size = Gauge(
            name="file_stat_last_file_size",
            documentation="Size in bytes of the latest modified file for the service",
            labelnames=label_list,
            registry=registry,
        )

        self.file_stat_oldest_modification_time = Gauge(
            name="file_stat_oldest_modification_time",
            documentation="Unix timestamp corresponding to the oldest "
            "file modification for the service",
            labelnames=label_list,
            registry=registry,
        )

        self.file_stat_oldest_file_size = Gauge(
            name="file_stat_oldest_file_size",
            documentation="Size in bytes of the oldest modified file for the service",
            labelnames=label_list,
            registry=registry,
        )

    def get_extra_labels(self):
        return self.yaml_file.get("extra_labels_definition", dict())

    def parse_yaml_config(self):
        list_config = dict()

        try:
            services = self.yaml_file["services"]
        except KeyError:
            raise KeyError('Error in your config file, "services" is missing.')

        for service, config in services.items():
            try:
                list_config[service] = ExporterConfig(
                    service=service,
                    driver=config["driver"]["name"],
                    driver_config=config["driver"].get("config", dict()),
                    extra_labels=self.extra_labels_default
                    | config.get("extra_labels", dict()),
                )
            except KeyError as e:
                raise KeyError(
                    f'Error in your config file, "{e.args[0]}" is missing in "{service}".'
                )

        return list_config

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            sleep(self.scrap_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with new values.
        """

        for service, config in self.exporter_configs.items():
            metrics = config.driver.get_metrics_safe()
            file_stat_count = int(metrics["file_stat_count"])
            file_stat_last_modification_time = int(
                metrics["file_stat_last_modification_time"]
            )
            file_stat_last_file_size = int(metrics["file_stat_last_file_size"])
            file_stat_oldest_modification_time = int(
                metrics["file_stat_oldest_modification_time"]
            )
            file_stat_oldest_file_size = int(metrics["file_stat_oldest_file_size"])

            try:
                self.file_stat_count.labels(**config.extra_labels).set(file_stat_count)
                self.file_stat_last_modification_time.labels(**config.extra_labels).set(
                    file_stat_last_modification_time
                )
                self.file_stat_last_file_size.labels(**config.extra_labels).set(
                    file_stat_last_file_size
                )
                self.file_stat_oldest_modification_time.labels(
                    **config.extra_labels
                ).set(file_stat_oldest_modification_time)
                self.file_stat_oldest_file_size.labels(**config.extra_labels).set(
                    file_stat_oldest_file_size
                )
            except ValueError:
                raise ValueError(
                    f"Extra label in service={service} not declared in extra_labels_definition"
                )
