#!/bin/sh

sipp -sf BLF.xml -s 52000 -p 5062 -trace_err -r 5 -m 2000 -trace_stat -nd -aa -inf BLF1.csv -i [servers]
