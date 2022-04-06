from random import sample
import re


s = '1102231990xxxxxxxx 123'
re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})', s)
