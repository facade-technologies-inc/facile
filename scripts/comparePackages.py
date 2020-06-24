import difflib
from pip._internal.operations import freeze

req = open('../requirements.txt')

tmp = freeze.freeze()
current = []
for package in tmp:
    current.append(package + '\n')

diff = difflib.ndiff(current, req.readlines())
list = ['\nNOTE:\n-: Current\n+: Requirement\n\n\n'] + [x for x in diff if (x.startswith('-') or x.startswith('+'))]
delta = ''.join(list)

print(delta)