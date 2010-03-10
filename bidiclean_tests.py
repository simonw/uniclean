import unittest
import bidiclean

bidi_tests = (
    (u'Normal string', u'Normal string'),
    (u'One explicit \u202a', u'One explicit \u202a\u202c'),
    (u'Two explicits \u202a\u202b',
        u'Two explicits \u202a\u202b\u202c\u202c'),
    (u'Three explicits \u202b\u202d\u202e', 
        u'Three explicits \u202b\u202d\u202e\u202c\u202c\u202c'),
    (u'Rogue pdf \u202c', u'Rogue pdf '),
    (u'Valid pdf \u202b\u202c', u'Valid pdf \u202b\u202c'),
    (u'One valid pdf, one rogue \u202b\u202c\u202c',
        u'One valid pdf, one rogue \u202b\u202c'),
)

class BidiCleanTest(unittest.TestCase):
    def test_naive(self):
        for input, expected in bidi_tests:
            actual = bidiclean.unicode_cleanup_rtl(input)
            self.assertEqual(expected, actual)
    
    def test_regex(self):
        for input, expected in bidi_tests:
            actual = bidiclean.unicode_cleanup_rtl_regex(input)
            self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
