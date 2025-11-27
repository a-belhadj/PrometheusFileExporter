from glob import glob
from os import path
from os.path import getmtime, getsize, isfile

from src.drivers.driver_interface import DriverInterface


class DriverLocal(DriverInterface):
    def __init__(self, driver_config):
        super().__init__(driver_config)
        self.dir_path = str(self.driver_config["path"])

    def get_files_list(self):
        # Get files corresponding to dir_path exp
        files = list(filter(isfile, glob(self.dir_path, recursive=True)))
        # Sort by creation_date
        files.sort(key=lambda x: -getmtime(x))
        return files

    def get_metrics(self):
        metrics = dict()

        files = self.get_files_list()
        # Files count
        file_count = len(files)

        # Latest backup info
        if file_count > 0:
            latest_file = files[0]
            latest_file_creation_date = path.getmtime(latest_file)
            latest_filesize = getsize(latest_file)

            oldest_file = files[-1]
            oldest_file_creation_date = path.getmtime(oldest_file)
            oldest_filesize = getsize(oldest_file)

        else:
            latest_filesize = 0
            latest_file_creation_date = 0

            oldest_filesize = 0
            oldest_file_creation_date = 0

        metrics["file_stat_last_modification_time"] = latest_file_creation_date
        metrics["file_stat_last_file_size"] = latest_filesize
        metrics["file_stat_oldest_modification_time"] = oldest_file_creation_date
        metrics["file_stat_oldest_file_size"] = oldest_filesize
        metrics["file_stat_count"] = file_count

        return metrics
