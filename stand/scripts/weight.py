#!/usr/bin/env python
import sys
import gspread

login = sys.argv[1]
pw = sys.argv[2]

gc = gspread.login(login, pw)

sh = gc.open('Weight')
worksheet = sh.worksheet('Weight')

print worksheet.get_all_values()
