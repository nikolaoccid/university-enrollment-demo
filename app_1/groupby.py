import itertools
from operator import itemgetter


def groupbykey(arr, key):
  arr = sorted(arr, key=itemgetter(key))
  return dict((k, list(g)) for k, g in itertools.groupby(arr, key=itemgetter(key)))

# l = [
#   {'a': 'tata', 'b': 'foo'},
#   {'a': 'pipo', 'b': 'titi'},
#   {'a': 'pipo', 'b': 'toto'},
#   {'a': 'tata', 'b': 'bar'}
# ]
# print(groupbykey(l, 'a'))
