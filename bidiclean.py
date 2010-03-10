explicits = set((
    u'\u202a', # LEFT-TO-RIGHT EMBEDDING
    u'\u202b', # RIGHT-TO-LEFT EMBEDDING
    u'\u202d', # LEFT-TO-RIGHT OVERRIDE
    u'\u202e', # RIGHT-TO-LEFT OVERRIDE
))
pdf = u'\u202c' # POP DIRECTIONAL FORMATTING

def unicode_cleanup_rtl(data):
    assert isinstance(data, unicode)
    count = 0
    clean = []
    for ch in data:
        if ch in explicits:
            count += 1
            clean.append(ch)
            continue
        if ch == pdf:
            if count:
                clean.append(ch)
                count -= 1
            continue
        clean.append(ch)
    
    for i in range(count):
        clean.append(pdf)
    
    return ''.join(clean)

import re

regex = re.compile(u'\u202a|\u202b|\u202d|\u202e|\u202c')
def unicode_cleanup_rtl_regex(data):
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

""" Cal's original PHP code:

function unicode_cleanup_rtl($data){

	#
	# LRE - U+202A - 0xE2 0x80 0xAA
	# RLE - U+202B - 0xE2 0x80 0xAB
	# LRO - U+202D - 0xE2 0x80 0xAD
	# RLO - U+202E - 0xE2 0x80 0xAE
	#
	# PDF - U+202C - 0xE2 0x80 0xAC
	#

	$explicits	= '\xE2\x80\xAA|\xE2\x80\xAB|\xE2\x80\xAD|\xE2\x80\xAE';
	$pdf		= '\xE2\x80\xAC';

	preg_match_all("!$explicits!",	$data, $m1, PREG_OFFSET_CAPTURE | PREG_SET_ORDER);
	preg_match_all("!$pdf!", 	$data, $m2, PREG_OFFSET_CAPTURE | PREG_SET_ORDER);

	if (count($m1) || count($m2)){

		$p = array();
		foreach ($m1 as $m){ $p[$m[0][1]] = 'push'; }
		foreach ($m2 as $m){ $p[$m[0][1]] = 'pop'; }
		ksort($p);

		$offset = 0;
		$stack = 0;
		foreach ($p as $pos => $type){

			if ($type == 'push'){
				$stack++;
			}else{
				if ($stack){
					$stack--;
				}else{
					# we have a pop without a push - remove it
					$data = substr($data, 0, $pos-$offset)
						.substr($data, $pos+3-$offset);
					$offset += 3;
				}
			}
		}

		# now add some pops if your stack is bigger than 0
		for ($i=0; $i<$stack; $i++){
			$data .= "\xE2\x80\xAC";
		}

		return $data;
	}

	return $data;
}
"""