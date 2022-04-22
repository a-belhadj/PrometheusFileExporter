from logging import getLogger
from utils import str_to_class


class ExporterConfig:
    def __init__(self, service, driver, driver_config, extra_labels):
        self.logging = getLogger(__name__)

        self.service = service
        self.driver_config = driver_config
        self.driver = str_to_class(driver)(driver_config=driver_config)
        self.extra_labels = extra_labels
        self.extra_labels["service"] = service

    def dump_conf(self, prefix):
        self.logging.info(f"{prefix}service={self.service}")
        self.logging.info(f"{prefix}driver={self.driver.__class__.__name__}")
        self.logging.info(f"{prefix}conf={self.driver_config}")
        self.logging.info(f"{prefix}extra_labels={self.extra_labels}")
