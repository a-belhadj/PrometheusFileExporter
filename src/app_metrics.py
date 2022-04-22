from time import sleep
import logging
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

        # Metrics backup_count
        self.backup_count = Gauge(name="file_stat_count",
                                  documentation="File count for the service",
                                  labelnames=label_list,
                                  registry=registry
                                  )
        self.latest_backup_timestamp = Gauge(name="file_stat_last_modification_time",
                                             documentation="Unix timestamp corresponding to the last "
                                                           "file modification for the service",
                                             labelnames=label_list,
                                             registry=registry
                                             )

        self.latest_backup_size = Gauge(name="file_stat_last_file_size",
                                        documentation="Size in bytes of the latest modified file for the service",
                                        labelnames=label_list,
                                        registry=registry
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
                    service = service,
                    driver = config["driver"]["name"],
                    driver_config = config["driver"].get("config", dict()),
                    extra_labels = self.extra_labels_default | config.get("extra_labels", dict())
                )
            except KeyError as e:
                raise KeyError(f'Error in your config file, "{e.args[0]}" is missing in "{service}".')

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
            metrics = config.driver.get_metrics()
            try:
                backup_count = int(metrics["backup_count"])
                latest_backup_timestamp = int(metrics["latest_backup_timestamp"])
                latest_backup_size = int(metrics["latest_backup_size"])
            except KeyError:
                raise KeyError(f'Method get_metrics in {config.driver.__class__.__name__} '
                               f'does not return a dict with required keys\n'
                               'get_metrics should returns a dict with backup_count, latest_backup_size '
                               'and latest_backup_timestamp '
                               '(e.g {"backup_count":10,"latest_backup_size":1000,'
                               ' "latest_backup_timestamp":1647253229})')
            try:
                self.backup_count.labels(**config.extra_labels).set(backup_count)
                self.latest_backup_timestamp.labels(**config.extra_labels).set(latest_backup_timestamp)
                self.latest_backup_size.labels(**config.extra_labels).set(latest_backup_size)
            except ValueError:
                raise ValueError(f'Extra label in service={service} not declared in extra_labels_definition')

            self.logging.info(
                f'service={service} backup_count={backup_count} latest_backup_timestamp={latest_backup_timestamp} latest_backup_size={latest_backup_size}')
