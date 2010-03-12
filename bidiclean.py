import re

explicits = (
    u'\u202a', # LEFT-TO-RIGHT EMBEDDING
    u'\u202b', # RIGHT-TO-LEFT EMBEDDING
    u'\u202d', # LEFT-TO-RIGHT OVERRIDE
    u'\u202e', # RIGHT-TO-LEFT OVERRIDE
)
pdf = u'\u202c' # POP DIRECTIONAL FORMATTING

regex = re.compile('|'.join(explicits + (pdf,)))
def bidiclean(data):
    """
    Ensure Unicode bidi characters are correctly balanced, as described by 
    Cal Henderson in http://www.iamcal.com/understanding-bidirectional-text/
    """
    count = [0] # Trick to work around Python's dodgy closure scoping
    def sub(m):
        ch = m.group(0)
        if ch == pdf:
            if count[0]:
                count[0] -= 1
                return ch
            else:
                return '' # Kill unbalanced pdfs
        else: # Not a pdf
            count[0] += 1
            return ch
    
    data = regex.sub(sub, data)
    return data + (pdf * count[0])
