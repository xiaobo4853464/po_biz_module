'''
Created on Oct 17, 2018

@author: xiaos5
'''
import unittest


class Sample(unittest.TestCase):
    def test(self):
        self.assertEquals("1", "1", "different")


if __name__ == '__main__':
    unittest.main()
