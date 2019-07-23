'''
Created on Oct 17, 2018

@author: xiaos5
'''
import unittest
class Sample(unittest.TestCase):
    def test_hello(self):
        print(Sample.num)
        a="hello"
#         self.assertEqual(a, "hello", "right")
        print(a)
        
if __name__ == '__main__':
    unittest.main()