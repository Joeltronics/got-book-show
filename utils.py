#!/usr/bin/env python3

"""
Game of Thrones chapters vs episodes chart generator
Copyright (c) 2013-2018, Joel Geddert

This script generates an HTML file of the table.

Software License:
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

A note from the author:
	The original chart generated by this code, as well as all remaining applicable
	source & asset files (except where noted), are licensed under a Creative Commons
	BY-SA 4.0 license <http://creativecommons.org/licenses/by-sa/4.0/>. If you are
	going to use any of this code to create a derivative work, please respect this
	CC license.
"""

import string
from typing import List, Callable, Optional, Union


_debug = False
warnings = []


def set_debug(val=True):
	global _debug
	_debug = val


def is_debug():
	return _debug


def warn(s: str):
	print('WARNING: %s' % s)
	warnings.append(s)


def debug_print(*args, **kwargs):
	if is_debug():
		print(*args, **kwargs)


def concatenate_lists(lists: List[List]) -> List:
	return sum(lists, [])


def find_unique(list: List, matching_function: Callable, throw_if_not_found=True):
	"""Find an item in a list, according to matching_function
	Assumes there is a single of the item in the list

	:param list: list to find in
	:param matching_function:
	:param throw_if_not_found: if True, will throw if not found; if false, will return None
	:return: the item
	:raises: ValueError if item is not in list or if multiple matches
	"""

	vals = [item for item in list if matching_function(item)]

	if len(vals) == 0:
		if throw_if_not_found:
			raise ValueError('Failed to find item in list')
		else:
			return None

	elif len(vals) > 1:
		raise ValueError('Multiple matches in list')

	return vals[0]


def htmlize_string(s: str) -> str:
	"""Replace characters with HTML escape characters"""
	return s.replace('&', '&amp;').replace('"', '&quot;')


def to_roman_numeral(num: int) -> str:
	if num < 1:
		raise ValueError("Can't convert zero or negative to roman numberal!")
	elif num > 39:
		raise NotImplementedError('to_roman_numeral not implemented for numbers >= 40')

	tens = num // 10
	ones = num % 10

	return ''.join(['X'] * tens) + ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'][ones]


# Inline unit tests
assert to_roman_numeral(1) == 'I'
assert to_roman_numeral(9) == 'IX'
assert to_roman_numeral(10) == 'X'
assert to_roman_numeral(28) == 'XXVIII'
assert to_roman_numeral(39) == 'XXXIX'


def display_string_len_approx(s: str) -> float:
	"""Determine approximate display string length

	Not going to be perfect because that requires not only rendering the text, but doing it in exactly the font (and
	kerning) the browser will use

	:param s: string to measure
	:return: string length, in typical characters
	"""

	n = 0.0
	# Iterate 1 character at a time
	for c in s:
		if c in '.\'':
			n += 0.33
		elif c in ' iIl':
			n += 0.5
		elif c in 'ACDGmw':
			n += 1.25
		elif c in 'MOQW':
			n += 1.5
		elif c in string.ascii_lowercase + string.ascii_uppercase + string.digits + '?':
			n += 1.0
		else:
			print('WARNING: unknown char ' + c + ' in string ' + s)
			n += 1.0

	return n


def abbrev_string(s: str, num_char: Union[float, int], prefix: Optional[str]=None) -> str:
	"""Abbreviate string to fit within num_char as best possible, trying not to split words if possible
	Will add "..." if abbreviated

	:param s: String to be abbreviated
	:param num_char: Max length (according to display_string_len_approx)
	:param prefix: Something to prepend to string, that will always be prepended in full (e.g. prepending book
	abbreviation or number to chapter name)

	:return: abbreviated string
	"""

	num_char = float(num_char)

	if not prefix:
		prefix = ''

	if prefix:
		prefix = prefix + ' '
		# Make room in character limit for prefix
		num_char -= display_string_len_approx(prefix)

	# Check if we even need to abbreviate at all
	if display_string_len_approx(s) <= num_char:
		return prefix + s

	# Once we reach this point, we know we need to abbreviate.
	# Make room in character limit for however many characters ellipsis will take
	num_char -= display_string_len_approx('...')

	# Try taking as many whole words as we can fit
	ss = s.split()
	num_words = len(ss)
	out_str = ''
	for n in range(num_words):
		if display_string_len_approx(' '.join(ss[0:n])) < num_char:
			out_str = ' '.join(ss[0:n])
		else:
			break

	# Now check if this ended up abbreviating to blank or just 'the'
	# If so, instead take as many characters as possible
	if (out_str == '') or (out_str.lower() == 'the'):
		out_str = ''
		for c in s:
			if display_string_len_approx(out_str + c) >= num_char:
				break
			out_str += c

	# If it ended on an apostrophe, remove it
	if out_str[-1:] == "'":
		out_str = out_str[:-1]

	out_str = prefix + out_str

	out_str += '...'

	debug_print("Abbreviating chapter '%s%s' as '%s'" % (prefix, s, out_str))

	return out_str


# Inline unit tests/examples
assert abbrev_string("The quick brown fox jumped over the lazy dogs", num_char=15) == "The quick brown..."
assert abbrev_string("antidisestablishmentarianism", num_char=15) == "antidisestablish..."
