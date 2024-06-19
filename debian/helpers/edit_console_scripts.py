#!/usr/bin/python3
#
# Helper tool to add f2pyX.YY to `console_scripts` section in entry_points.txt
#
# it expects 3 positional arguments:
#
# 1. the path to the `entry_points.txt` script
# 2. the option name to set
# 3. the value associated with that option name

import configparser
import sys


class CaseSensitiveConfigParser(configparser.ConfigParser):
    optionxform = staticmethod(str)


entry_points = CaseSensitiveConfigParser()
entry_points.read_file(open(sys.argv[1]))

if (sys.argv[2], sys.argv[3]) not in entry_points.items('console_scripts'):
    entry_points.set('console_scripts', sys.argv[2], sys.argv[3])


with open(sys.argv[1], 'w') as f:
    entry_points.write(f)

