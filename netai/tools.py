from tabulate import tabulate as render_table
import shutil

def display(data):
	
	return Display(data)


def Display(data):

	data = DF(data)

	if not data:
		print(" No Data")
		return

	if not isinstance(data,list):
		print(str(data)[:500])
		return
	
	rows = len(data)

	pages = Paginate(data)
	total = len(pages)
	count = 0
	rcount = 0

	for page in pages:
	   
		table = GetTable(data[page["start"]:page["end"]])
		print(render_table(table["data"],headers=table["headers"]))
		
		if (total < 2) or Continue(page['msg']):
			pass
		else:
			break


	print("")


def Continue(msg):

	inp = input(f" {msg} | [c]ancel")
	
	if inp.lower() in ["c","cancel"]:
		return False
	
	return True
	
def GetTable(data):

	cols = [key for key in data[0].keys()]
	res = []

	for x in data:
		row = GetRow(x,cols)
		res.append(row)

	return {"data":res,"headers":cols}

def DF(data):
	
	if isinstance(data,dict):
		res = []
		for k,v in data.items():
			res.append({"key":k,"val":v})

		return res

	if isinstance(data,list):      
		return data

	return []

def GetRow(rec,cols):

	res = []

	for key in cols:
		res.append(GetValue(rec.get(key)))

	return res


def GetValue(val):
	if val == None:
		res = ""
	else:
		res = str(val)

	if len(res) > 32:
		res = res[:30] + ".."

	return res


def Paginate(data):

	limit = get_term_height() - 4

	rows = len(data)
	res = []
	for n1 in range(0,rows,limit):
		if (n1 + limit) > rows:
			n2 = rows
		else:
			n2 = n1 + limit
		res.append({"start":n1,"end":n2}) 


	pages = len(res)
	page = 0

	for x in res:
		page+=1
		x["page"] = page
		x["msg"] = f"Page: {page:,} of {pages:,} | rows: {x['end']:,} of {rows:,}"

	return res



def get_term_height(default: int = 24) -> int:
	try:
		return shutil.get_terminal_size().lines
	except OSError:
		return default



def SetValue(data, path, value):
	"""
	Set a value at the specified nested dictionary path.

	- Existing value is replaced.
	- Missing path elements are created.
	- Existing branches are preserved.
	- If an intermediate path element exists but is not a dictionary,
	  it is replaced with a dictionary.
	"""

	key_path = KeyPath(path)

	if not key_path:
		return

	current = data

	# Walk/create the path up to the final key
	for key in key_path[:-1]:
		if key not in current or not isinstance(current[key], dict):
			current[key] = {}

		current = current[key]

	# Set or replace the final value
	current[key_path[-1]] = value

	return data


def KeyPath(vals):

	if isinstance(vals,str):
		return vals.split(".")

	if isinstance(vals,list):
		return vals
	
