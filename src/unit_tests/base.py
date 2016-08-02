import unittest

class ExplorerTestBase(unittest.TestCase):
    
    def assertEq(self, expected, actual, msg=''):
        self.assertEqual(expected, actual, "%s\nExpected: %s\nActual: %s"%(msg, expected, actual))

    def assertSourceURL(self, actual, matched=[], unmatched=[]):
        self.assertEq([matched, unmatched], actual, 
                         "The URLs do not match")
