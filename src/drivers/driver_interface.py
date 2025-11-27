from logging import getLogger


class DriverInterface:
    def __init__(self, driver_config):
        self.logging = getLogger(__name__)
        self.driver_config = driver_config

    def get_metrics(self):
        list_of_metrics = [
            "file_stat_count",
            "file_stat_last_file_size",
            "file_stat_last_modification_time",
            "file_stat_oldest_file_size",
            "file_stat_oldest_modification_time",
        ]
        raise NotImplementedError(
            f"Method get_metrics not implemented in {self.__class__.__name__}\n"
            f"get_metrics should returns a dict with {', '.join(list_of_metrics)} "
            '(e.g {"file_stat_count":10,"file_stat_last_file_size":1000, '
            '"file_stat_last_modification_time":1647253229})'
        )
        return dict()

    def get_metrics_safe(self):
        metrics = self.get_metrics()
        list_of_metrics = [
            "file_stat_count",
            "file_stat_last_file_size",
            "file_stat_last_modification_time",
            "file_stat_oldest_file_size",
            "file_stat_oldest_modification_time",
        ]
        for metric in list_of_metrics:
            if metric not in metrics:
                raise KeyError(
                    f"Method get_metrics in {self.__class__.__name__} "
                    f'does not return a dict with required key "{metric}"\n'
                    f"get_metrics should returns a dict with {', '.join(list_of_metrics)} "
                    '(e.g {"file_stat_count":10,"file_stat_last_file_size":1000, '
                    '"file_stat_last_modification_time":1647253229})'
                )
        return metrics
