#!/bin/sh

now=$(date +%Y%m%d%H%M)
killall sipp
zip -r ../simulator_$now.zip *
rm -rf *_.*
rm -rf *_errors.*
