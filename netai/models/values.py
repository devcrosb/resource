import json

### Validators:
### ------------------------------------

def isFloat(value):

	if Float(value):
		return True


def isInt(value):

	if Int(value):
		return True

def isString(value):

	if isinstance(value,str):
		return True

def isAlpha(value):

	try:
		if value.isalpha():
			return True
	except:
		pass


def isSafe(value):

	if Safe(value):
		return True
	
def isSemantic(value):

	if Semantic(value):
		return True

def hasAlpha(value):

	if not isString(value):
		return False

	if value.isdigit():
		return False

	for val in value[:255]:
		if val.isalpha():
			return True

	return False

def isKey(value):

	if Key(value):
		return True



### Parsers:
### ------------------------------------

def Key(value):

	try:
		val = value.lower().strip()
	except:
		return

	if len(val) == 0:
		return

	val = val.replace("-","_").replace(" ","_")

	if val in DATA["keys"]:
		return val

	if DATA["key"].get(val):
		return DATA["key"][val]


def Semantic(value):

	if Safe(value) and hasAlpha(value):
		return True
	

def Valid(value):

	if value is None:
		return False
	
	if not isinstance(value,str):
		return True
	
	value = value.strip()

	if len(value) == 0:
		return False
	
	if value.isalnum():
		return True

	if hasAlpha(value):
		return True

	return False


def Lower(value):
	
	val = String(value)

	return val.lower()
	

def Int(value):

	try:
		return int(value)
	except:
		pass

def Float(value):

	try:
		return float(value)
	except:
		pass
	
def String(value):

	if value is None:
		return ""

	if isinstance(value,(list,dict)):
		return json.dumps(value)

	return str(value)



def Safe(value):

	if not isString(value):
		return

	if len(value) > 64:
		return

	if value.isalnum():
		return value
	
	if len(value) < 2:
		return

	if not value[0].isalnum():
		return

	if not value[-1].isalnum():
		return

	val = value.replace("-","")

	if len(val) == 0:
		return
	
	if val.isdigit():
		return
	
	if val.isalnum():
		return value
	

DATA = {
	"key":{
		"ip_address":"ip",
		"netmask":"mask",
		"net_mask":"mask",
		"network_address":"network",
		"street_address":"street",
		"zip":"post_code",
		"zip_code":"post_code"
	},
	"keys":{
		"ip","network","mask","dns",
		"hostname","email","fqdn","domain",
		"country","country_id","region","city","state","steet","post_code",
		"port","tcp_port","udp_port"
	}
}

