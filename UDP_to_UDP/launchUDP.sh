#!/bin/bash

path="$(dirname "$(realpath "$0")")";
initSleep=30
script="OpenPMU_UDP_to_UDP.py"


echo PATH: $path
cd $path

echo Initial sleep, give time for system to boot
sleep $initSleep

echo Starting loop

while true; do
python3 $script
sleep 1

done
