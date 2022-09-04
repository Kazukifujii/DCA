#!/bin/bash
echo -n "csvadress="
read csvadress
python3 cluster_show.py -csvn $csvadress