import os
import json
import requests
import netai.config as config


def Request(message,**args):
	
	api = API()
	
	return api.Request(message,**args)


def Models():
	
	api = API()
	
	return api.Models()


class API:
	def __init__(self):

		self.conf = config.Load("openai.test")

		self.url = self.conf.Get("url")

		self.headers = {
			"Authorization": f"Bearer {self.conf.Get('auth.key')}",
			"Content-Type": "application/json",
		}

	def Models(self):
		
		resp = requests.get(f"{self.url}/models",headers=self.headers)
		
		code = resp.status_code

		if code == 200:
			status = "true"
		else:
			status = "false"


		try:
			data = resp.json()
			try: data = data["data"]
			except: pass
		except:
			try: msg = str(resp.text)
			except: msg = "Error"
			data = {"message":msg}

		

		return {"status":status,"code":200,"data":data,"role":"system","type":"table"}


	def Request(self,text,**args):

		message = InputText(text)
		if not message:
			return {"code":400,"status":"false","content":"Invalid or empty message","role":"system"}
		

		model = args.get("model") or self.conf.Get("model") or "gpt-5.1"
		payload = {"model": model,"input": []}

		sys_msg = args.get("system_message") or self.conf.Get("system.message")
		if sys_msg:
			payload["input"].append({
				"role": "system",
				"content": [{"type": "input_text", "text": sys_msg}]
			})

		role = args.get("role") or "user"
	
		payload["input"].append({
			"role": role,
			"content": [{"type": "input_text", "text": message}],
		})

		temp = args.get("temperature") or self.conf.Get("request.temperature")

		if temp != None:
			payload["temperature"] = temp

		max_tokens =  args.get("max_output_tokens") or self.conf.Get("request.max_output_tokens")

		if max_tokens != None:
			payload["max_output_tokens"] = max_tokens

		extra = args.get("extra") or self.conf.Get("extra")		

		if extra and isinstance(extra,dict):
			payload.update(extra)

		timeout = args.get("timeout") or self.conf.Get("timeout") or 60

		res = requests.post(
			f"{self.url}/responses",
			headers=self.headers,
			json=payload,
			timeout=timeout
		)

		code = res.status_code
		
		if code != 200:
			try: msg = res.text
			except:	msg = "Unspecified"

			return self.Error("request",code,msg)

		try:
			data = res.json()
		except Exception as e:
			return self.Error("request",500,str(e))
		

		content = ResponseText(data)
		
		if not content:
			return self.Error("response",500,"The response message was empty.")
	
		return {"status":"true","code":200,"content":content,"role":"assistant","type":"text"}


	def Error(self,method,code,message):

		return {"status":"false","code":code,"content":f"{method}-error: {message}","role":"system"}



def ResponseText(data):

	lines = []
	for item in data.get("output", []):
		for content in item.get("content", []):
			if content.get("type") == "output_text":
				lines.append(content.get("text", ""))

	text = "\n".join(lines).strip()

	if Semantic(text):
		return text


def InputText(text):
		
	if not text:
		return 
	
	if isinstance(text,list):
		try:
			text = "\n".join(text)	
		except:
			text = json.dumps(list)

	elif isinstance(text,dict):
		text = json.dumps(text)

	else:
		text = str(text)
		
	
	text = " " + text.replace("\r"," ") + " "
	text = " " + text.replace("\n\n",". ") + " "
	text = " " + text.replace("\n",". ") + " "

	for char in ["?","!",";",";",":",",",")","]","}",">"]:
		text = text.replace(char,f"{char} ")

	lines = []
	line = []

	for val in text.split(" "):
		
		if EndChar(val):
			if line:
				line[-1]+=val
				lines.append(" ".join(line))
				line = []
		elif EndWord(val):
			line.append(val)
			lines.append(" ".join(line))
			line = []
		elif Semantic(val):
			line.append(val)

	if line:
		line[-1]+="." 
		lines.append(" ".join(line))

	if lines:
		return " ".join(lines)


def Semantic(val):

	if not isinstance(val,str) or (len(val) == 0):
		return
	
	for char in val:
		if char.isalnum():
			return True
		

def EndWord(val):
	
	if not isinstance(val,str) or (len(val) < 2):
		return

	return EndChar(val[-1])


def EndChar(val):

	if not isinstance(val,str) or (len(val) != 1):
		return

	if val in {"?","!",";",";",":",",",")","]","}",">"}:
		return True
