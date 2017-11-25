# Description
Tool to generate reports of OpenStreetMap

*Example: generate report of the total length of residential and living_street highways in OpenStreetMap without name.*

# Installation
```sh
pip install .
```

# Previous steps
## Tools needed
- osm2pgsql: https://github.com/openstreetmap/osm2pgsql
- postgis

## Data preparation
- Create database (dbname, dbuser, dbpass) with the postgis and hstore extensions
- Edit report.conf to set your conection data (dbname, dbuser, dbpass), area name and area/subarera admin_levels
- Download data: http://download.geofabrik.de/index.html
- Load data to database:
```sh
osm2pgsql -s --cache-strategy sparse -G --hstore -E 4326 -l -C 2048 -S report.style -d dbname data-planet.osm.pbf -H localhost -U dbuser -W
```

# Usage
- Execute
```sh
manuel towns/report.conf
```
