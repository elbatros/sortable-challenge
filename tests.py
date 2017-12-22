import unittest
from collections import Counter
from rollup import RollupTable
from StringIO import StringIO


class TestGetColumnValues(unittest.TestCase):
    def setUp(self):
        self.all_columns = ["y", "m", "d"]
        self.columns = ["y", "d"]
        self.rollup = RollupTable(self.columns)
        self.rollup.set_header(self.all_columns)

    def test_extracts_correct_values_from_row(self):
        result = self.rollup.get_column_values(["2017", "1", "2", "3"])
        self.assertEqual(("2017", "2"), result)

class TestPrefixesFromRow(unittest.TestCase):
    def test_gets_all_prefixes(self):
        rollup = RollupTable(["y", "m", "d"])
        prefixes = rollup.prefixes_from_row(["2016", "1", "1"])
        self.assertEqual((), next(prefixes))
        self.assertEqual(("2016", ), next(prefixes))
        self.assertEqual(("2016", "1"), next(prefixes))
        self.assertEqual(("2016", "1", "1"), next(prefixes))
        with self.assertRaises(StopIteration):
            next(prefixes)

class TestAddRow(unittest.TestCase):
    def setUp(self):
        self.all_columns = ["y", "m", "d"]
        self.columns = self.all_columns[:-1]
        self.rollup = RollupTable(self.columns)
        self.rollup.set_header(self.all_columns)

    def test_add_row(self):
        self.rollup.add_row(["2017", "1", "1", "1"])
        self.rollup.add_row(["2016", "2", "2", "1"])
        self.rollup.add_row(["2016", "3", "3", "1"])
        self.assertEqual(3, self.rollup.get_count(()))
        self.assertEqual(2, self.rollup.get_count(("2016", )))
        self.assertEqual(1, self.rollup.get_count(("2016", "2")))
        self.assertEqual(0, self.rollup.get_count(("2016", "1")))

class TestOutput(unittest.TestCase):
    def setUp(self):
        all_columns = [
            ["y", "m", "d"],
            Counter({
                (): 1,
                ("2016", ): 1,
                ("2016", "1"): 1,
                ("2016", "1", "1"): 1,
            }),
            (
                "y\tm\td\tvalue\n"
                "\t\t\t1\n"
                "2016\t\t\t1\n"
                "2016\t1\t\t1\n"
                "2016\t1\t1\t1\n"
            )
        ]
        self.cases = [all_columns]

    def test_example(self):
        for columns, counter, expected in self.cases:
            rollup = RollupTable(columns, counter)
            out = StringIO()
            rollup.output(out)
            result = out.getvalue()
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
