import sys
s = 'import sys\ns = {!r}\nsys.stdout.write(s.format(s))\n'
sys.stdout.write(s.format(s))