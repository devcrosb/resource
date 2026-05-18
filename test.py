from netai.nlp import NLP,SetKV
from netai.tools import Display
import json



def Test1():

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


if __name__ == "__main__":
	Test1()
	
    



