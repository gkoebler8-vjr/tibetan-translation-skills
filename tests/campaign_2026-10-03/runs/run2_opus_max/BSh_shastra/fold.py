import sys, unicodedata
def fold(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
print('\0'.join(fold(a) for a in sys.argv[1:]), end='')
