from nlp import NLP
import json

nlp = NLP()

def Match(value,vals):

	value = str(value).strip()

	if value in vals:
		return True
	
	if value.lower() in vals:
		return True
	

def CLI():

	while True:

		sentence = input("Enter an English sentence: ").strip()
		
		if len(sentence) == 0:
			print("")
		
		elif Match(sentence,["quit","q","exit","x"]):
			print("Bye..\n")
			return
		
		else:
			results = nlp.Parse(sentence)

			print(json.dumps(results,indent=4))

def Test():

	text = '''
		The meeting starts at 9.
		What time does the meeting start?
		Start the meeting now.
		Please send the report.
		Could you open the window?
		Don't touch that.
		You should start the meeting.
		How beautiful this is!
		Select all locations and then summarize.
	'''
	
	
	for x in nlp.Parse(text):
		print(json.dumps(x,indent=4))
		inp = input(" < Hit [enter] or [q]uit >")
		if inp.lower() == "q":
			break

def main():
	Test()

if __name__ == "__main__":
	main()
