from netai.parse import GetType, SetType, Key


class NLP:

	def __init__(self):

		info = LoadInfo()

		self.limit = 3
		self.value = info["value"]
		self.type = info["type"]


	def Parse(self,text):

		lines = TextLines(text)

		res = []
		count = 0

		for line in lines:
		
			rec = self.ParseLine(line)
		
			if rec:
				count+=1
				rec["line"] = count
				res.append(rec)

		return res
	
	def ParseLine(self,line):

		line,stop = GetStop(line)

		params = {}
		vals = []
		last = None

		for x in self.LineVals(line):
			
			if x.get("key"):
				key = x["key"]
				SetKV(params,key,x["value"])
				val = "{" f"{key}: {x['value']}" + "}"

			elif x["usage"] == "syntactic":
				val = x["value"]

			elif not last:
				val = "<" + x["value"] + ">"

			elif last["type"] == "key":
				key = last["value"]
				SetKV(params,key,x["value"])
				val = "{" f"{key}: {x['value']}" + "}"
				vals = vals[:-1]

			else:
				val = "<" + x["value"] + ">"

			vals.append(val)

			last = x

		if not vals:
			return
		
		vals = " ".join(vals)

		return {"text":line,"meaning":vals,"stop":stop,"params":params}
	
	
	def LineVals(self,line):

		line = line.lower()
		vals = line.split(" ")

		if not vals:
			return []

		result = []

		while True:

			token,count = self.NextVal(vals)
			result.append(self.Get(token))

			if len(vals) <= count:
				return result

			vals = vals[count:]

	def Get(self,token):

		if self.value.get(token):
			return self.value[token].copy()

		wtype = GetType(token)

		value = SetType(token,wtype)

		if value is None:
			return

		value = str(value)

		rec = {"value":token,"type":wtype}

		x = self.type.get(wtype) or {"usage":"semantic","class":"value","key":Key(wtype)}

		for key in ["usage","class","key"]:
			if x.get(key):
				rec[key] = x.get(key)


		return rec
			
			

	def NextVal(self,vals):

		if len(vals) == 1:
			return vals[0],1

		if len(vals) < self.limit:
			nx = len(vals)
		else:
			nx = self.limit

		for n in range(nx,0,-1):
			token = "_".join(vals[0:n])

			if self.value.get(token):
				return token,n
			
		return vals[0],1

def SetKV(params,key,value):
	
	if not params.get(key):
		params[key] = value
	
	elif isinstance(params[key],list):
		params[key].append(value)
	
	elif str(value) != str(params[key]):
		params[key] = [params[key],value]


def GetStop(text):

	if len(text) == 0:
		stop = None
	
	elif isStop(text[-1]):
		stop = text[-1]
		text = text[:-1]
	else:
		stop = "<br>"

	return text, stop

def isStop(val):
		
	if val in {"!","?",".",";",":"}:
		return True
	
def TextLines(text):

	text = text.replace("\r\n","\n")
	text = text.replace("\r","\n")
	text = text.replace("\n"," ")
	text = text.replace("\t"," ")
	text = text.replace("_"," ")    

	vals = []
	for val in text.split(" "):
		if len(val) > 0:
			vals.append(val)

	text = " ".join(vals)

	eol = "<-|end|->"

	for char in ["!","?",". "]:
		text = text.replace(char,f"{char}{eol}")

	text = text.replace("  "," ")

	text = text.replace("\n\n",eol) + " "

	res = []
	for line in text.split(eol):
		line = line.strip()
		if len(line) > 0:
			res.append(line)

	return res




def LoadInfo():
	
	res = {"value":{},"type":{}}


	for wtype, vals in DATA["type"].items():
		
		res["type"][wtype] = {"usage":"syntactic","class":"word"}

		for val in vals:
			if not res["value"].get(val):
				res["value"][val] = {"type":wtype,"value":val,"usage":"syntactic","class":"word"}

	res["type"]["key"] = {"usage":"semantic","class":"param"}

	for key in DATA["param"]:

		wtype = key.replace("_","-") 
		res["type"][wtype] = {"key":key,"usage":"semantic","class":"param"}

		if key in ["ip","mac","network"]:
			res["value"][f"{key}_address"] = {"type":"key","value":key,"usage":"semantic","class":"param"}

		res["value"][key] = {"type":"key","value":key,"usage":"semantic","class":"param"}

	return res


DATA = {
	"param":[
		"ip","mac","network","email",
		"hostname","cname",
		"fqdn","domain",
		"system_name","system_id",
		"asset_name","asset_id",
		"interface_name","interface_id",
		"vendor","model",
		"time","date","datetime",
		"building","city","country","region","timezone"
		"building_id","country_id","region_id","location_id",
		"port","tcp_port","udp_port"
	],
	"type":{
		"imperative":[
			"select","get","fetch","download","find","retrieve","take","please"
		],
		"interorgative":[
			"do", "does", "did", "is", "are", "am", "was", "were",
			"have", "has", "had", "can", "could", "will", "would",
			"shall", "should", "may", "might", "must"
		],
		"w5":[
			"who", "what", "when", "where", "why", "how", "which", "whom", "whose"
		],
		"article":[
			"a","the","that","this","those"
		],
		"prepostion":[
			"on","at","in","before","after","under","over","in","at","between","inside","to","into","through","from","toward"
		],
		"pronoun":[
			"i","you","he","she","it","we","they","me",
			"you","him","her","it","us","them",
			"mine","yours","myself","their","my"
		],
		"conjunction":[
			"for","and","or","nor","not","but","yet","so"
			"both","either","whether","neither","such","that","rather","than"
		],
		"stop":["!","?",".",";",":"],
		"hyphen":[".","-","/"],
	}
}