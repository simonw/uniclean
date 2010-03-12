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
    pass

i = 0
for input, expected in bidi_tests:
    def test(self):
        actual = bidiclean.bidiclean(input)
        self.assertEqual(expected, actual)
    test.__name__ = 'test_%d' % i
    setattr(BidiCleanTest, 'test_%d' % i, test)
    i += 1

if __name__ == '__main__':
    unittest.main()
