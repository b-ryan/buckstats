#!/usr/bin/env python
import os, sys
import gspread

_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_dir, '..'))

from stand.model import Weight
from stand.app import db

login = sys.argv[1]
pw = sys.argv[2]

gc = gspread.login(login, pw)

sh = gc.open('Weight')
worksheet = sh.worksheet('Weight')

Weight.query.delete()

for value in worksheet.get_all_values()[1:]:
    weight = Weight(
        date=value[0],
        weight=float(value[2]),
        goal_weight=(float(value[1]) if value[1] != '' else None),
        notes=(value[3] if value[3] != '' else None),
    )
    db.session.add(weight)

db.session.commit()
