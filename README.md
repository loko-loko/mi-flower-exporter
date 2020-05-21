# Mi Flower Exporter

## How to use

### Config file

Flower Exporter work with config file whose contain flower information (Name and Mac address).

You can find an example of a config file in: `templates/config.yml`.

### Options

See options of Flower Exporter:
- `-c|--config`: Config file
- `-p|--port` (Optional): Port for the webserver scraped by Prometheus [Default: `9250`]
- `-d|--debug` (Optional): Debug Mode [Default: `False`]
- `--refresh-interval` (Optional): Refresh interval in seconds for data collect [Default: `1800`]
- `--dump-path` (Optional): Path for the dumps [Default: `/tmp/mi_flower_exporter.cache`]


### Run with Docker

Ensure bluetooth service is stop on your host:
```
systemctl status bluetooth
systemctl stop bluetooth
```

Run container with privileged right, host's network and a config file with your flower info:
```bash
docker run --net=host --privileged -v $(pwd)/config.yml:/exporter/config.yml --name mi_flower_exporter -ti mi-flower-exporter
```

Once container is started, you can check state with comand:
```
curl 127.0.0.1:9250
```

### Logs

You can check exporter status with `docker logs` command.

Example:
```
$ docker logs mi_flower_exporter -f
Starting system message bus: dbus.
Starting bluetooth: bluetoothd.
2020/05/21 14:34:19  INFO    - Mi-Flower Exporter Start (PID:20) ..
2020/05/21 14:34:19  INFO    - Prometheus web server started: my_host:9250
2020/05/21 14:34:19  INFO    - Getting data from Flower_ext_1 [C4:00:00:00:00:01]
2020/05/21 14:34:19  INFO    - Getting data from Flower_ext_2 [C4:00:00:00:00:02]
2020/05/21 14:34:21  INFO    - Exporting Completed
2020/05/21 14:36:09  INFO    - Done getting data for Flower_ext_1
2020/05/21 14:36:13  INFO    - Done getting data for Flower_ext_2
```