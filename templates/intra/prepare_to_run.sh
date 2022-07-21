#!/bin/sh

now=$(date +%Y%m%d%H%M)
killall sipp
zip -r simulator.zip ../simulator/*
mv simulator.zip ../simulator_$now.zip
rm -rf *_.*
