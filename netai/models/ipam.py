import re
from netai.models.values import Int,isString,isAlpha,hasAlpha,isSafe,Safe
from netai.models.geo import isCountryID


### Validators
### ==================================================


def isEmail(value):

	if Email(value):
		return True

def isFQDN(value):

	if FQDN(value):
		return True

def isHostname(value):

	if Hostname(value):
		return True

def isDomain(value):
	
	if Domain(value):
		return True
	
def isNetwork(value):

	if Network(value):
		return True
	
def isIP(value):

	if IP(value):
		return True

def isTLD(value):

	if TLD(value):
		return True

def isSuffix(value):

	if Suffix(value):
		return True

def isEmailName(value):

	if EmailName(value):
		return True

def isEmail(value):
	if Email(value):
		return True

def isMask(value):

	res = Int(value)

	if 0 < res < 33:
		return res

def isDNS(value):

	if DNS(value):
		return True


### Parsers
### ==================================================

def Email(value):

	if not isString(value):
		return 

	
	if value.count("@") != 1:
		return

	try:
		name,domain = value.split("@",1)
	except:
		return
	
	if isEmailName(name) and isDomain(domain):
		return True


def EmailName(value):

	if not isString(value):
		return 
	
	if len(value) > 64:
		return

	if PATTERN["mail"].fullmatch(value):
		return value


def Hostname(value):
	
	if not isSafe(value):
		return

	if len(value) > 64:
		return 

	
	if value[0] != "alpha":
		return 
	
	if value[-1] != "digit":
		return
	
	for val in value.split("-"):
		if not HostType(val):
			print(f" > Bad Host Type: '{val}' in '{value}'")
			return

	return value


def HostType(value):

	try:
		val = value.lower()
	except:
		return
	
	if len(val) < 2:
		return
	
	if TLD(val):
		return
	
	if PFX(val):
		return 
	
	if val.isalnum():
		return value


def PFX(value):

	try:
		val = value.lower()
	except:
		return
	
	if val in {"www","ftp","http","https","ssh","mail","api"}:
		return value

def FQDN(value):

	if not isString(value):
		return 

	if value.count(".") < 2:
		return 

	hostname,domain = value.split(".",1)

	if isHostname(hostname) and isDomain(domain):
		return value


def Domain(value):

	if not isString(value):
		return 
	
	value = value.lower().strip()

	if len(value) > 255:
		return 

	vals = value.split(".")

	if len(vals) < 2:
		return 

	if not TLD(vals[-1]):
		return

	if (len(vals) > 2) and Hostname(vals[0]):
		return

	res = []
	for val in vals:
		if not Suffix(val):
			return

	return value


def Suffix(value):
	
	if isSafe(value) and hasAlpha(value):
		return value


def TLD(value):
	
	try:
		val = value.lower()
	except:
		return

	if not isAlpha(value):
		return 

	if value in DATA["tld"]:
		return value
	
	if isCountryID(value):
		return value


def Network(value):

	try:
		ip, mask = value.split("/",1)
	except:
		return 

	ip = IP(ip)	
	mask = Mask(mask)

	if ip and mask:
		return f"{ip}/{mask}"

def DNS(value):

	val = str(value)

	if val in {"8.8.8.8","8.8.8.4","1.1.1.1","1.1.1.2"}:
		return True
	

def IP(value):
	
	if not isinstance(value,str):
		return
	
	if not value.count(".") != 4:
		return
	
	value = value.split("/")[0]

	vals = []

	for val in value.split("."):

		try: val = int(val)
		except: return

		if (not vals) and (254 < val < 1):
			return
		elif 255 < val < 0:
			return

		vals.append(str(val))

	return ".".join(vals)


def Mask(value):


	if isMask(value):
		return int(value)


	try:
		ip, mask = value.split("/")[1]
	except:
		return 
		
	if IP(ip) and isMask(mask):
		return int(mask)



DATA = {
	"tld":{
		"com",
		"org",
		"net",
		"edu",
		"gov",
		"mil",
		"int",
		"info",
		"biz",
		"io",
		"ai",
		"app",
		"dev",
		"co",
		"me",
		"tv",
		"xyz",
		"online",
		"store",
		"blog",
		"site",
		"tech",
		"cloud",
		"shop",
		"news",
		"media",
		"finance",
		"solutions",
		"services",
		"digital",
		"agency",
		"group",
		"company",
		"network",
		"systems",
		"software",
		"world",
		"today",
		"live",
		"space",
		"email",
		"pro",
		"name",
		"mobi",
		"travel",
		"jobs",
		"museum",
		"aero",
		"arpa"
	}
}


PATTERN = {
	"mail":re.compile(r"^(?!\.)(?!.*\.\.)([A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]{1,64})(?<!\.)$")
}
