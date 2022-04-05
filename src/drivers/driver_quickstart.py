from src.drivers.driver_interface import DriverInterface

class DriverQuickstart(DriverInterface):

    # Overriding the constructor is optional
    # def __init__(self, driver_config):
    #     super().__init__(driver_config)
    #     self.logging.info(self.driver_config)


    def get_metrics(self):
        metrics = dict()
        metrics["backup_count"] = 1
        metrics["latest_backup_timestamp"] = 2
        metrics["latest_backup_size"] = 3
        return metrics
