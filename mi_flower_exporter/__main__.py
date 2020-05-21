# /usr/bin/env python3

import os
from sys import stderr
from argparse import ArgumentParser
from yaml import safe_load
from time import sleep
from string import Template

from loguru import logger as log
from prometheus_client import REGISTRY

from mi_flower_exporter.collector import FlowerCollector, DataDumpCollect
from mi_flower_exporter.prometheus import CollectMany, init_http_server
from mi_flower_exporter.utils import get_config, create_dump_path, get_flowers_to_collected


# Default vars
_REFRESH_INTERVAL = 1800
_EXPORTER_PORT = 9250
_DUMP_PATH = "/tmp/mi_flower_exporter.cache"


def arg_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Config file with Mi-Flora info"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=_EXPORTER_PORT,
        help=f"Port for the webserver scraped by Prometheus [Default: {_EXPORTER_PORT}]"
    )
    parser.add_argument(
        "--refresh-interval",
        type=int,
        default=_REFRESH_INTERVAL,
        help=f"Refresh interval in seconds for data collect [Default: {_REFRESH_INTERVAL}]"
    )
    parser.add_argument(
        "--dump-path",
        default=_DUMP_PATH,
        help=f"Path for the dumps [Default: {_DUMP_PATH}]"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Debug Mode"
    )
    return parser.parse_args()


def main():
    error_msg = "Collector could not run"
    collector_pid = os.getpid()
    pid_file = "/var/run/mi-flower-exporter.pid"
    # Get args
    args = arg_parser()
    # init logger
    log_level = "DEBUG" if args.debug else "INFO"
    log.remove()
    log.add(
        stderr,
        level=log_level,
        format="{time:YYYY/MM/DD HH:mm:ss}  {level:<7} - {message}"
    )
    # Check pid
    if os.path.isfile(pid_file):
        log.error(f"{error_msg}: Existing pid file is present")
        exit(1)
    # Get flower config
    config = get_config(args.config)
    # Generate dump file template path
    create_dump_path(args.dump_path)
    f_template = Template(
        os.path.join(args.dump_path, f"$name.{collector_pid}.dump")
    )
    # Get flowers to collect
    flowers = get_flowers_to_collected(config)
    # Init prometheus http server
    log.info(f"Mi-Flower Exporter Start (PID:{collector_pid}) ..")
    init_http_server(args.port)
    # Start data collect with interval
    for flower in flowers:
        data_collect = DataDumpCollect(
            name=flower,
            mac=config[flower]["mac"],
            file_dump=f_template.substitute(name=flower.lower()),
            refresh_interval=args.refresh_interval
        )
        data_collect.start()
    # Wait dump files creation
    log.debug("Wait for first dump file creation ..")
    sleep(2)
    # Start flower prometheus collector
    collectors = []
    for flower in flowers: 
        collector = FlowerCollector(
            name=flower,
            mac=config[flower]["mac"],
            file_dump=f_template.substitute(name=flower.lower())
        )
        collectors.append(collector)
    REGISTRY.register(CollectMany(collectors))
    log.info(f"Exporting Completed")

    while True:
        sleep(30)

if __name__ == "__main__":
    main()
