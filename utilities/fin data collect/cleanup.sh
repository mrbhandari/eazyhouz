#!/bin/bash
python combinefiles.py
python csvtotsv.py result.csv result.tsv
cut -f1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,31,32,33 result.tsv |grep -v "MLS Rules require that you be registered with a verified email"|sort|uniq > result_clean.tsv
cat result_clean.tsv |cut -f6,24|sort|uniq|cut -f1|uniq -c