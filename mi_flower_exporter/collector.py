import pickle
from time import time, sleep
from os import rename

from prometheus_client.core import GaugeMetricFamily, CollectorRegistry
from loguru import logger
from threading import Thread

from btlewrap import GatttoolBackend
from .miflora.miflora_poller import MiFloraPoller

_BACKEND = GatttoolBackend


class DataDumpCollect(Thread):

    def __init__(self, name, mac, file_dump, refresh_interval=1800):
        Thread.__init__(self)
        self.name = name
        self._mac = mac
        self._file_dump = file_dump
        self._refresh_interval = refresh_interval

    def run(self):
        logger.debug(f"Starting data gather thread for: {self.name}")
        # Init dump file
        self._dump_data_to_file(cfile=self._file_dump, data={"collect": 0})
        # Start data collect with interval
        while True:
            # Init data
            data = {"collect": 0}
            start_time = time()
            try:
                # Poll mi-flower data
                data.update(self._poll_data(name=self.name, mac=self._mac))
            except Exception as e:
                logger.error(f"Error getting data for {self.name}: {e}")
            else:
                data["poll_time"] = time() - start_time
            # Write new dump
            logger.debug(f"Data for {self.name}: {data}")
            new_file_dump = f"{self._file_dump}.new"
            self._dump_data_to_file(cfile=new_file_dump, data=data)
            rename(new_file_dump, self._file_dump)
            logger.debug(f"Done dumping data for {self.name} to {self._file_dump}")
            # Waiting for the next collect
            sleep(self._refresh_interval)

    @staticmethod
    def _dump_data_to_file(cfile, data):
        with open(cfile, "wb+") as f:
            pickle.dump((data, ), f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _poll_data(name, mac):
        logger.info(f"Getting data from {name} [{mac}]")
        poller = MiFloraPoller(mac=mac, backend=_BACKEND)
        data = {
            "collect": 1,
            "temperature": float(poller.parameter_value("temperature")),
            "moisture": int(poller.parameter_value("moisture")),
            "light": int(poller.parameter_value("light")),
            "conductivity": int(poller.parameter_value("conductivity")),
            "battery": int(poller.parameter_value("battery"))
        }
        return data


class FlowerCollector():

    def __init__(self, name, mac, file_dump):
        self.name = name
        self._mac = mac
        self._file_dump = file_dump

    def flower_metrics(self):
        # Get flower data from cache file
        with open(self._file_dump, "rb") as f:
            data = pickle.load(f)[0]
        # Generate metrics
        for metric, value in data.items():
            gauge = GaugeMetricFamily(
                f"mi_flower_{metric}",
                f"Mi Flower Metrics",
                labels=["name", "mac"]
            )
            gauge.add_metric([self.name, self._mac], value)
            yield gauge

    def collect(self):
        yield from self.flower_metrics()
