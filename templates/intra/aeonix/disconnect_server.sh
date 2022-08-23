#!/bin/sh

sudo iptables -A OUTPUT -d [server] -j DROP
sudo iptables -A INPUT -s [server] -j DROP
