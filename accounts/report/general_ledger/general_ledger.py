# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import flt, add_days
from webnotes import _
from accounts.utils import get_balance_on

def execute(filters=None):
	account_details = webnotes.conn.get_value("Account", filters["account"], 
		["debit_or_credit", "group_or_ledger"], as_dict=True) if filters.get("account") else None
	validate_filters(filters, account_details)
	
	columns = get_columns()
	data = []
	if filters.get("group_by"):
		data += get_grouped_gle(filters)
	else:
		data += get_gl_entries(filters)
		if data:
			data.append(get_total_row(data))

	if account_details:
		data = [get_opening_balance_row(filters, account_details.debit_or_credit)] + data + \
			[get_closing_balance_row(filters, account_details.debit_or_credit)]

	return columns, data
	
def validate_filters(filters, account_details):
	if account_details and account_details.group_or_ledger == "Ledger" \
			and filters.get("group_by") == "Group by Account":
		webnotes.throw(_("Can not filter based on Account, if grouped by Account"))
		
	if filters.get("voucher_no") and filters.get("group_by") == "Group by Voucher":
		webnotes.throw(_("Can not filter based on Voucher No, if grouped by Voucher"))
	
def get_columns():
	columns = ["Posting Date:Date:100", "Account:Link/Account:200", "Debit:Float:100", 
		"Credit:Float:100", "Voucher Type::120", "Voucher No::160", "Link::20", 
		"Cost Center:Link/Cost Center:100", "Remarks::200"]
	# translate only the label part of column
	return map(lambda c: ":".join([_(c[0]), c[1]]), map(lambda s: s.split(':', 1) if s.count(':')>=1 else [s, ''], columns))
		
def get_opening_balance_row(filters, debit_or_credit):
	opening_balance = get_balance_on(filters["account"], add_days(filters["from_date"], -1))
	return get_balance_row(opening_balance, debit_or_credit, "Opening Balance")
	
def get_closing_balance_row(filters, debit_or_credit):
	closing_balance = get_balance_on(filters["account"], filters["to_date"])
	return get_balance_row(closing_balance, debit_or_credit, "Closing Balance")
	
def get_balance_row(balance, debit_or_credit, balance_label):
	if debit_or_credit == "Debit":
		return ["", balance_label, balance, 0.0, "", "", ""]
	else:
		return ["", balance_label, 0.0, balance, "", "", ""]
		
def get_gl_entries(filters):
	gl_entries = webnotes.conn.sql("""select 
			posting_date, account, debit, credit, voucher_type, voucher_no, cost_center, remarks 
		from `tabGL Entry`
		where company=%(company)s 
			and posting_date between %(from_date)s and %(to_date)s
			{conditions}
		order by posting_date, account"""\
		.format(conditions=get_conditions(filters)), filters, as_list=1)
		
	for d in gl_entries:
		icon = """<a href="%s"><i class="icon icon-share" style="cursor: pointer;"></i></a>""" \
			% ("/".join(["#Form", d[4], d[5]]),)
		d.insert(6, icon)
		
	return gl_entries
			
def get_conditions(filters):
	conditions = []
	if filters.get("account"):
		lft, rgt = webnotes.conn.get_value("Account", filters["account"], ["lft", "rgt"])
		conditions.append("""account in (select name from tabAccount 
			where lft>=%s and rgt<=%s and docstatus<2)""" % (lft, rgt))
	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")
	
	return "and {}".format(" and ".join(conditions)) if conditions else ""
		
def get_grouped_gle(filters):
	gle_map = {}
	gle = get_gl_entries(filters)
	for d in gle:
		gle_map.setdefault(d[1 if filters["group_by"]=="Group by Account" else 5], []).append(d)
		
	data = []
	for entries in gle_map.values():
		subtotal_debit = subtotal_credit = 0.0
		for entry in entries:
			data.append(entry)
			subtotal_debit += flt(entry[2])
			subtotal_credit += flt(entry[3])
		
		data.append(["", "Total", subtotal_debit, subtotal_credit, "", "", ""])
	
	if data:
		data.append(get_total_row(gle))
	return data
	
def get_total_row(gle):
	total_debit = total_credit = 0.0
	for d in gle:
		total_debit += flt(d[2])
		total_credit += flt(d[3])
		
	return ["", _("Total Debit/Credit"), total_debit, total_credit, "", "", ""]