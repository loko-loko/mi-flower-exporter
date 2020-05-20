import socket
from loguru import logger

from prometheus_client import Info, start_http_server

import mi_flower_exporter

def init_http_server(port):
    hostname = socket.gethostname()
    logger.debug(f"Start Prometheus web server: {hostname}:{port} ..")
    
    start_http_server(port)

    prometheus_info = Info(
        'mi_flower_exporter',
        'Mi-Flower Prometheus exporter'
    )
    prometheus_info.info({
        'version': mi_flower_exporter.__version__,
        'running_on': hostname
    })

    logger.info(f"Prometheus web server started: {hostname}:{port}")

class CollectMany:

    def __init__(self, collectors):
        self.collectors = collectors

    def collect(self):
        for collector in self.collectors:
            yield from collector.collect()