#!/bin/bash
# gen_open.sh KEY... : open imagery for sat60 keys
cd /home/claude/v60
export GDAL_HTTP_CAINFO=/root/.ccr/ca-bundle.crt
for k in "$@"; do
  read lon lat d <<<$(python3 -c "from sat60 import SP;print(*SP['$k'])")
  [ -f satO/$k.jpg ] || python3 /home/claude/v62/open_imagery.py $lon $lat $d 1620 2880 satO/$k.jpg > satO/$k.log 2>&1 &
done
wait
