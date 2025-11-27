from src.drivers.driver_interface import DriverInterface


class DriverQuickstart(DriverInterface):
    # Overriding the constructor is optional
    # def __init__(self, driver_config):
    #     super().__init__(driver_config)
    #     self.logging.info(self.driver_config)

    def get_metrics(self):
        metrics = dict()
        metrics["file_stat_count"] = 1
        metrics["file_stat_last_modification_time"] = 2
        metrics["file_stat_last_file_size"] = 3
        metrics["file_stat_oldest_modification_time"] = 4
        metrics["file_stat_oldest_file_size"] = 5
        return metrics
