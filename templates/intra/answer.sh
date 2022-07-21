#!/bin/sh

sipp -sf uas_All.xml -s 52000 -p 5061 -trace_err -trace_stat -nd -aa -inf call_answer.csv -i [servers]
