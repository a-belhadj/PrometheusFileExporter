from logging import getLogger


class DriverInterface:

    def __init__(self, driver_config):
        self.logging = getLogger(__name__)
        self.driver_config = driver_config

    def get_metrics(self):
        raise NotImplementedError(f'Method get_metrics not implemented in {self.__class__.__name__}\n'
                                  'get_metrics should returns a dict with backup_count, '
                                  'latest_backup_size and latest_backup_timestamp '
                                  '(e.g {"backup_count":10,"latest_backup_size":1000, '
                                  'ExporterConfig"latest_backup_timestamp":1647253229})')
