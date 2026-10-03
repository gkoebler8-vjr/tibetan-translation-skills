# run-local wrapper: beats.py with extra stress entries (skill lexicon left untouched)
import sys, os
sys.path.insert(0, os.path.expanduser('~/.claude/skills/tibetan-verse/tools'))
import lexicon
lexicon.STRESS.update({
 'departure': (3, [2], []), 'journey': (2, [1], []), 'defeat': (2, [2], []),
 'rebirth': (2, [2], []), 'tushita': (3, [2], []), 'dharmakaya': (4, [3], [1]),
})
import beats
sys.exit(beats._main(sys.argv))
