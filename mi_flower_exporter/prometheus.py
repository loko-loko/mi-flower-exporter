import socket
from loguru import logger as log

from prometheus_client import Info, start_http_server

from mi_flower_exporter import __version__ as VERSION

def init_http_server(port):
    hostname = socket.gethostname()
    log.debug(f"Start Prometheus web server: 0.0.0.0:{port} (Host:{hostname}) ..")
    start_http_server(port)
    prometheus_info = Info(
        "mi_flower_exporter",
        "Mi-Flower Prometheus exporter"
    )
    prometheus_info.info({
        "version": VERSION,
        "running_on": hostname
    })
    log.info(f"Prometheus web server started: {hostname}:{port}")

class CollectMany:

    def __init__(self, collectors):
        self.collectors = collectors

    def collect(self):
        for collector in self.collectors:
            yield from collector.collect()