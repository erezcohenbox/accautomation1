#!/bin/sh

sipp -sf uas_All.xml -s 52000 -p 5061 -trace_err -trace_stat -nd -aa -inf call_answer.csv -i [servers]
#sipp -sf uas_All.xml -s 52000 -p 5061 -trace_msg -trace_shortmsg -trace_err -trace_error_codes -trace_error_codes -trace_calldebug -trace_screen option -nd -aa -inf call_answer.csv -i [servers]