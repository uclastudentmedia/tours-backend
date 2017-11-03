# Valhalla Mapzen Server Setup


## Installation

Download a map section that includes all important features from
[OpenStreetMap](https://www.openstreetmap.org/export). This should come as a
`.osm` file.

Use `osmconvert` to convert the `.osm` file to a `.pbf` file.

Follow the instructions on the [valhalla repo](https://github.com/valhalla/valhalla) to install Valhalla.


## Project-specific configuration

In `valhalla.json`, edit the line
```
"listen": "tcp://*:8080"
```
to use an available port.

Create `/etc/init/valhalla.conf`:
```
description "Valhalla Mapzen routing"

start on (local-filesystems and net-device-up IFACE=eth0)
stop on runlevel [!12345]

respawn

setuid www-data
setgid www-data

# Change this to the directory where valhalla is installed
chdir /var/www/html/valhalla

exec valhalla_route_service valhalla.json 1
```

Start the routing service
```
service valhalla start
```

Set up Apache for port forwarding. The port in your Apache config should match
the port in `valhalla.json`. See [apache.md](apache.md).
