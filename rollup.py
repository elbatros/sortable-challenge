#!/usr/bin/env python2

import sys
from collections import Counter
from operator import itemgetter


class RollupTable(object):
    def __init__(self, columns, counter=None):
        if not counter:
            counter = Counter()
        self.__counter = counter
        self.__columns = columns

    def set_header(self, header):
        if not self.__columns:
            self.__columns = header[:-1]

        self.__column_indexes = [header.index(c) for c in self.__columns]

    def add_row(self, row):
        count = int(row[-1])
        values = self.get_column_values(row)
        for prefix in self.prefixes_from_row(values):
            self.__counter[prefix] += count

    def get_count(self, prefix):
        return self.__counter[prefix]

    def output(self, out=sys.stdout):
        columns = list(self.__columns)
        columns.append("value")
        out.write("\t".join(columns))
        out.write("\n")
        for prefix, value in sorted(self.__counter.iteritems()):
            row = list(prefix)
            padding = [""] * (len(self.__columns) - len(row))
            row.extend(padding)
            row.append(str(value))
            out.write("\t".join(row))
            out.write("\n")

    def get_column_values(self, row):
        return itemgetter(*self.__column_indexes)(row)

    def prefixes_from_row(self, row):
        for i in xrange(len(self.__columns) + 1):
            yield tuple(row[:i])


def main():
    columns = sys.argv[1:]

    is_first_line = True
    rollup = RollupTable(columns)
    for line in sys.stdin:
        row = line.split("\t")
        if is_first_line:
            is_first_line = False
            rollup.set_header(row)
            continue

        rollup.add_row(row)

    rollup.output()


if __name__ == "__main__":
    main()
