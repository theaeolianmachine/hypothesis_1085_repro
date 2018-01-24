import unittest

from repro_package.hit_by_unittest import sum


class TestSumNoHypothesis(unittest.TestCase):
    def test_add(self):
        self.assertEquals(sum(2, 5), 7)


if __name__ == '__main__':
    unittest.main()
