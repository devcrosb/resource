import json


class Config:

	def __init__(self,*args,**kwargs):
		
		self.data = {}
		self.file = {}
		self.path = kwargs.get("path") or "../config"

		for name in args:
			path = f"{self.path}/{name}.json" 
			self.data[name] = json.loads(open(path).read())
			self.file[name] = path


	def Get(self,arg=None):

		return GetTree(self.data,arg)
	

class Load:
	
	def __init__(self,tree,**args):

		self.tree = tree

		name = tree.split(".",1)[0]

		self.path = args.get("path") or "../config" + f"/{name}.json"

		data = {name:json.loads(open(self.path).read())}
		
		self.data = GetTree(data,tree)

	
	def Get(self,arg=None):

		return GetTree(self.data,arg)



def GetTree(res,keys):
		
	if not keys:
		return res
	
	for key in keys.split("."):
		try:
			res = res[key]
		except:
			return
			
	return res
	