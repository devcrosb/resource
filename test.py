import json


def Test1():

	from netai.nlp import NLP,SetKV
	from netai.tools import Display

	text = '''
		John bought a car.
		Mary is a doctor.
		Open the file.
		Can you send me the file?
		The meeting starts at 3pm.
		Send Bob the report.
		Block 192.168.1.10 on the firewall.
		Allow 10.0.0.0/24 through the gateway.
		Resolve server01.prod.example.com using 8.8.8.8.
		Evaluate hostname server03.prod.example.com
		Email admin@example.com the report.
		Open port 443 on firewall01.
		I saw the man with the telescope.
		What time is the meeting?
		'''

	nlp = NLP()

	data = nlp.Parse(text)

	Display(data)

	params = {}
	for x in data:
		for k,v in x["params"].items():
			SetKV(params,k,v)

	print(json.dumps(params,indent=4))


def Test2():

	import driver.chatgpt as chatgpt

	resp = chatgpt.Request("List the capital cities in Australia.")

	msg = f"{resp['role'].upper()} | {resp['code']} | {resp['status']}:"
	line = (len(msg) + 3) * "-"

	print(f"\n {msg}\n {line}\n\n{resp['content']}\n\n{line}\n")

def Test3():

	from netai.tools import Display
	import driver.chatgpt as chatgpt

	resp = chatgpt.Models()

	#print(json.dumps(resp,indent=4))
	Display(resp["data"])


if __name__ == "__main__":
	Test3()
	





