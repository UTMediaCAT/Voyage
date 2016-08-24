import unittest

class ExplorerTestBase(unittest.TestCase):
    
    def assertEq(self, expected, actual, msg=''):
        self.assertEqual(expected, actual, "%s\nExpected: %s\nActual: %s"%(msg, expected, actual))

    def assertSources(self, actual, matched=[], unmatched=[], msg=''):
        self.assertEq([matched, unmatched], actual, 
                         "The sources do not match " + msg)
