import re
import spacy


#Sentence Types: 
# declarative: Statement
# interrogative: Question
# imperative: Command


class NLP:

	def __init__(self):


		self.tokenize = spacy.load("en_core_web_sm")

		self.pattern = {
			"integer": re.compile(r"^\d+$"),
			"decimal": re.compile(r"^\d+\.\d+$"),
			"ip-address": re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$"),
			"mac-address": re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"),
			"network-address": re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$"),
			"email": re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$"),
			"fqdn": re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"),
		}

		# Map spaCy POS to your schema
		self.map = {
			"pos":{
				"NOUN": "noun",
				"VERB": "verb",
				"ADJ": "adjective",
				"ADV": "adverb",
				"PRON": "pronoun",
				"ADP": "preposition",
				"CCONJ": "conjunction",
				"SCONJ": "conjunction",
				"DET": "determiner",
				"PROPN": "name",
			}
		}



	def Parse(self,text):

		text = text.strip()
		if not text:
			return

		res = []		
		for tokens in self.GetTokens(text):
			x = self.EvalTokens(tokens)
			if x:
				res.append(x)

		return res


	def GetTokens(self,text):			
		
		text = text.replace("\r","\n")
		text = text.replace("\n\n","\n ")
		text = text.replace("\t"," ")
		text = text.replace("\n ","<$eol>")
		text = text.replace("\n"," ")

		for dm in [".","?","!",";"]:
			val = f"{dm} "
			if val in text:
				text = text.replace(val,f"{dm}<$eol>")

		for dm in ["and then,","and then","then,","then","*","-",">"]:
			val = f" {dm} "
			if val in text:
				text = text.replace(val,"<$eol>")

		res = []

		for subtext in text.split("<$eol>"):
		
			subtext = subtext.strip()

			if len(subtext) == 0:
				subtext = None
			elif subtext.count(" ") == 0:
				subtext = f"search {subtext}"
			
			tokens = self.Tokens(subtext)

			if tokens:
				res.append(tokens)

		return res


	def EvalTokens(self,tokens):

		if self.isSelector(tokens):
			resp = {"type":"interrogative","action":"select"}

		elif self.isInterogative(tokens):
			resp = {"type":"interrogative","action":"query"}
		
		elif self.isImperative(tokens):
			resp = {"type":"imperative","action":"command"}

		elif self.isNegImperative(tokens):
			resp = {"type":"neg-imperative","action":"negate"}

		else:
			resp = {"type":"declarative","action":"store"}

		resp["tokens"] = JoinTokens(tokens)

		return resp


	def isSelector(self,tokens):

		if len(tokens) < 2:
			return 
		
		first = tokens[0].lower_
		
		if (first == "please") and (len(tokens) > 2):
			first = tokens[1].lower_

		if first in {"select","get","fetch","download","find","query","retrieve","take"}:
			return True
		

	def isInterogative(self,tokens):

		#1: Eval Interrogatives (questions/queries)

		if tokens[-1].text == "?":
			return True

		first = tokens[0].lower_

		wh_words = {"who", "what", "when", "where", "why", "how", "which", "whom", "whose"}
		aux_starters = {
			"do", "does", "did", "is", "are", "am", "was", "were",
			"have", "has", "had", "can", "could", "will", "would",
			"shall", "should", "may", "might", "must"
		}
		
		if first in wh_words:
			return True
		
		if first in aux_starters and len(tokens) >= 2:
			# e.g. "Can you help me"
			return True
		
	def isImperative(seklf,tokens):

		#2: Eval Imperatives:
		# Common imperative markers:
		# - starts with "please"
		# - begins with a base verb
		# - implied subject "you" instead of explicit grammatical subject

		first = tokens[0].lower_

		if first == "please":
			return "imperative"

		# Ignore leading adverbs like "please", "kindly", "just", "now"
		lead_idx = 0
		ignorable = {"please", "kindly", "just", "now"}
		doc = []
		for x in tokens:
			doc.append(x)

		while lead_idx < len(tokens) and tokens[lead_idx].lower_ in ignorable:
			lead_idx += 1

		if lead_idx < len(tokens):
			lead = tokens[lead_idx]

			if isBaseVerb(lead):
				# Look for an explicit nominal subject attached to the root/lead verb.
				has_subject = any(tok.dep_ in {"nsubj", "nsubjpass", "csubj", "expl"} for tok in doc)
				if not has_subject:
					return True

	def isNegImperative(self,tokens):

		text = JoinTokens(tokens)

		# Special negative imperatives: "Don't move.", "Do not enter."
		if re.match(r"^(do not|don't)\b", text.lower()):
			return True


	def Tokens(self,text):

		if not text:
			return []

		doc = self.tokenize(text)
		result = [t for t in doc if not t.is_space]

		if len(result) > 0:
			return result



	def TokenType(self,token):
		
		text = token.text

		# 1. Special regex-based types
		for t, pattern in self.pattern.items():
			if pattern.match(text):
				return t

		# 2. Punctuation / brackets
		if token.is_punct:
			if text in "()[]{}":
				return "bracket"
			return "punctuation"

		# 3. POS-based types
		if token.pos_ in POS_MAP:
			return POS_MAP[token.pos_]

		# 4. Fallback
		return "label"
	
def JoinTokens(tokens):

	res = []

	for token in tokens:
		res.append(token.text)
	return " ".join(res)


def isBaseVerb(token) -> bool:
	"""
	Heuristic: imperatives often begin with a base-form verb.
	"""
	return (
		token.pos_ in {"VERB", "AUX"}
		and token.tag_ in {"VB"}
	)

