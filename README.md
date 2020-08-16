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
- `--logs` (Optional): Enable writing logs to a file [Default: `False`]
- `--log-path <path>` (Optional): Log path [Default: `/var/log/mi-flower-exporter`]
- `--refresh-interval <seconds>` (Optional): Refresh interval in seconds for data collect [Default: `1800`]
- `--dump-path <path>` (Optional): Path for the dumps [Default: `/tmp/mi_flower_exporter.cache`]

### Run with systemctl

Ensure bluetooth service is running on your host:
```
systemctl status bluetooth
```

Customize (If needed) and copy service template to systemd services path.
```
sudo cp templates/mi-flower-exporter.service /lib/systemd/system/
```

Create config and log path:
```
sudo mkdir /{etc,var/log}/mi-flower-exporter
```

Customize and copy config file in config path:
```
sudo cp templates/config.yml /etc/mi-flower-exporter/
```

Reload, enable and start service:
```
sudo systemctl daemon-reload
sudo systemctl enable mi-flower-exporter
sudo systemctl start mi-flower-exporter
```

Check service status:
```
sudo systemctl status mi-flower-exporter
```

Once service is running, you can check data with following command:
```
curl 127.0.0.1:9250
```

### Run with Docker

Ensure bluetooth service is stop on your host:
```
systemctl status bluetooth
systemctl disable bluetooth
systemctl stop bluetooth
```

Run container with privileged right, host's network and a config file with your flower info:
```bash
docker run --net=host --privileged -v $(pwd)/config.yml:/exporter/config.yml --name mi_flower_exporter -ti mi-flower-exporter
```

Once container is running, you can check data with the following command:
```
curl 127.0.0.1:9250
```

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
