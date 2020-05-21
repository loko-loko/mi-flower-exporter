#!/bin/bash

CONFIG_FILE="/exporter/config.yml"

# Start dbus
/etc/init.d/dbus start

# Start bluetoothd
/etc/init.d/bluetooth start

# Run exporter with args
/usr/local/bin/mi-flower-exporter --config $CONFIG_FILE $@