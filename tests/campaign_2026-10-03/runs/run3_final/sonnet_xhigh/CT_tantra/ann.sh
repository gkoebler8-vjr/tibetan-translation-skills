#!/bin/zsh
# usage: ann.sh Uxx [extra args]
D="<scratchpad>/runs/run3_final/sonnet_xhigh/CT_tantra"
u=$1; shift
s=$(date +%H:%M:%S)
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "$(cat $D/units/$u.txt)" "$@" > $D/dict/$u.txt 2>&1
echo "- tibdict annotate $u $@  start $s end $(date +%H:%M:%S)" >> $D/runlog.md
