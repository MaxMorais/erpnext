# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import msgprint, _

def execute(filters=None):
	account_map = get_account_map()
	columns = get_columns(account_map)
	data = []
	suppliers = webnotes.conn.sql("select name from tabSupplier where docstatus < 2")
	for supplier in suppliers:
		row = [supplier[0]]
		for company in sorted(account_map):
			row.append(account_map[company].get(supplier[0], ''))
		data.append(row)

	return columns, data

def get_account_map():
	accounts = webnotes.conn.sql("""select name, company, master_name 
		from `tabAccount` where master_type = 'Supplier' 
		and ifnull(master_name, '') != '' and docstatus < 2""", as_dict=1)

	account_map = {}
	for acc in accounts:
		account_map.setdefault(acc.company, {}).setdefault(acc.master_name, {})
		account_map[acc.company][acc.master_name] = acc.name

	return account_map

def get_columns(account_map):
	columns = ["Supplier:Link/Supplier:120"] + \
		[(company + ":Link/Account:120") for company in sorted(account_map)]

	# translate only the label part of column
	return map(lambda c: ":".join([_(c[0]), c[1]]), map(lambda s: s.split(':', 1) if s.count(':')>=1 else [s, ''], columns))