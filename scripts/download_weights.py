#!/usr/bin/env python
import os, sys
import gspread

_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_dir, '..'))

from stand.model import Weight

login = sys.argv[1]
pw = sys.argv[2]

gc = gspread.login(login, pw)

sh = gc.open('Weight')
worksheet = sh.worksheet('Weight')

for value in worksheet.get_all_values()[1:]:
    weight = Weight(
        date=value[0],
        weight=value[2],
        goal_weight=value[1],
        notes=value[3],
    )
    print weight
