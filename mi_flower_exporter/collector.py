from os import rename
from time import time, sleep
from threading import Thread

from prometheus_client.core import GaugeMetricFamily
from prometheus_client.core import CollectorRegistry
from loguru import logger as log
from btlewrap.bluepy import BluepyBackend

from miflora.miflora_poller import MiFloraPoller

from mi_flower_exporter.utils import write_dump_data_to_file
from mi_flower_exporter.utils import read_dump_data_from_file


BLT_BACKEND = BluepyBackend


class DataDumpCollect(Thread):

    def __init__(self, name, mac, file_dump, refresh_interval=1800):
        Thread.__init__(self)
        self.name = name
        self._mac = mac
        self._file_dump = file_dump
        self._refresh_interval = refresh_interval

    def run(self):
        log.debug(f"Starting data gather thread for: {self.name}")
        # Init dump file
        write_dump_data_to_file(dump_file=self._file_dump, data={"collect": 0})
        # Start data collect with interval
        while True:
            # Init data
            data = {"collect": 0}
            start_time = time()
            try:
                # Poll mi-flower data
                data.update(self._poll_data(name=self.name, mac=self._mac))
            except Exception as e:
                log.error(f"Error getting data for {self.name}: {e}")
            else:
                log.info(f"Done getting data for {self.name}")
                # Update data with new value if collect OK
                data.update({
                    "collect": 1,
                    "poll_time": time() - start_time
                })
            # Write new dump
            log.debug(f"Data for {self.name}: {data}")
            new_file_dump = f"{self._file_dump}.new"
            write_dump_data_to_file(dump_file=new_file_dump, data=data)
            rename(new_file_dump, self._file_dump)
            log.debug(f"Done dumping data for {self.name} to {self._file_dump}")
            # Waiting for the next collect
            sleep(self._refresh_interval)


    @staticmethod
    def _poll_data(name, mac):
        log.info(f"Getting data from {name} [{mac}]")
        poller = MiFloraPoller(mac=mac, backend=BLT_BACKEND)
        data = {
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
        data = read_dump_data_from_file(dump_file=self._file_dump)
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
