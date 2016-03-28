"""
pylinq.query
~~~~~~~~~~~~

This module implements the query functions.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from itertools import chain, dropwhile, groupby, islice, takewhile

TYPE = ["concat",
        "difference",
        "distinct",
        "groupby",
        "groupjoin",
        "intersect",
        "join",
        "orderby",
        "orderbydesc",
        "reverse",
        "select",
        "selectmany",
        "skip",
        "skipwhile",
        "take",
        "takewhile",
        "union",
        "where"]


class _Query(object):

    def __init__(self):
        self.types = {}
        for i, query_type in enumerate(sorted(TYPE)):
            self.types[query_type] = 1 << i

    def __getattr__(self, name):
        return self.types[name]

    def parse(self, iterator, query):
        if query[0] == self.where:
            iterator = filter(query[1], iterator)
        elif query[0] == self.select:
            iterator = map(query[1], iterator)
        elif query[0] == self.skip:
            iterator = islice(iterator, query[1], None)
        elif query[0] == self.take:
            iterator = islice(iterator, query[1])
        elif query[0] == self.concat:
            iterator = chain(iterator, query[1])
        elif query[0] == self.skipwhile:
            iterator = dropwhile(query[1], iterator)
        elif query[0] == self.takewhile:
            iterator = takewhile(query[1], iterator)
        elif query[0] == self.orderby:
            iterator = sorted(iterator, key=query[1])
        elif query[0] == self.orderbydesc:
            iterator = sorted(iterator, key=query[1], reverse=True)
        elif query[0] == self.groupby:
            iterator = groupby(
                sorted(iterator, key=query[1]), key=query[1])
        elif query[0] == self.selectmany:
            iterator = chain.from_iterable(map(query[1], iterator))
        elif query[0] == self.reverse:
            iterator = reversed(list(iterator))
        elif query[0] == self.distinct:
            seen = {}

            def comparator(item):
                key = query[1](item)
                if key in seen:
                    return False
                seen[key] = 1
                return True
            iterator = filter(comparator, iterator)
        elif query[0] == self.union:
            seen = {}

            def comparator1(item):
                key = query[2](item)
                if key in seen:
                    return False
                seen[key] = 1
                return True

            def comparator2(item):
                key = query[3](item)
                if key in seen:
                    return False
                seen[key] = 1
                return True
            iterator = chain(filter(comparator1, iterator),
                             filter(comparator2, query[1]))
        elif query[0] == self.intersect:
            seen = dict(zip(map(query[3], query[1]), query[1]))

            def comparator(item):
                key = query[2](item)
                if key in seen:
                    return True
                return False
            iterator = filter(comparator, iterator)
        elif query[0] == self.join:
            def join(iterable, query):
                for key1, group1 in groupby(sorted(iterable, key=query[2]), key=query[2]):
                    for item1 in group1:
                        for key2, group2 in groupby(
                                sorted(query[1], key=query[3]), key=query[3]):
                            if key1 == key2:
                                for item2 in group2:
                                    yield query[4](item1, item2)
            iterator = join(iterator, query)
        elif query[0] == self.groupjoin:
            def join(iterable, query):
                for key1, group1 in groupby(sorted(iterable, key=query[2]), key=query[2]):
                    for item1 in group1:
                        for key2, group2 in groupby(
                                sorted(query[1], key=query[3]), key=query[3]):
                            if key1 == key2:
                                yield query[4](item1, group2)
            iterator = join(iterator, query)
        elif query[0] == self.difference:
            seen = dict(zip(map(query[3], query[1]), query[1]))

            def comparator(item):
                key = query[2](item)
                if key in seen:
                    return False
                seen[key] = 1
                return True
            iterator = filter(comparator, iterator)
        else:
            raise ValueError("Unknown query operation: %s" % query[0])
        return iterator

Query = _Query()
