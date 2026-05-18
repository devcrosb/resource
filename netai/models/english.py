from netai.models.ascii import Ascii
import re


### Validators:
### ============================================================


def isWord(value):

	if Word(value):
		return True


def isVowel(val):

	if Vowel(val):
		return True


def isWordType(val):

	if WordType(val):
		return True


def isWordGroup(val):
	
	if WordGroup(val):
		return True


def isSyntax(val):
	if Syntax(val):
		return True
	

### Parsers
### ============================================================


def Word(value):

	value = Normalize(value)
	if not value:
		return

	for val in value.split("-"):
		if not WordType(val):
			return
		
	return value

def Normalize(text):

	value = Ascii(text)
	if not value:
		return
	
	value = value.strip()

	if len(value) > 0:
		return value


def Vowel(val):
	  
	try:
		v = val.lower()
	except:
		return

	if v in {"a","e","i","o","u"}:
		return val


def WordType(value):

	try:
		val = value.lower()
	except:
		return

	if not val.isalpha():
		return
	
	if len(val) > 32:
		return 

	if val in {"a","i"}:
		return value

	if len(val) < 2:
		return

	if WordGroup(val):
		return value

	cons = 0
	vowel = 0
	n = 0

	for char in val:
		n+=1

		if isVowel(char):
			vowel+1

		elif (char == "y") and (n > 1):
			vowel+=1

		else:
			cons+=1

		if cons and vowel:
			return value


### Helpers
### =============================================

def Strip(value):

	value = value.strip().lower()

	if len(value) == 0:
		return
	
	if len(value) == 1:
		return DATA["alias"].get(value) or value

	if len(value) < 2:
		return value
	
	if value.isalpha():
		return value

	if not value[0].isalpha():
		value = value[1:]

	if not value[-1].isalpha():
		value = value[:-1]

	return value 


def DefineWord(value: str) -> str:
	
	if not isinstance(value,str):
		return
	
	word = Word(value)

	if not word:
		return
	
	if word.count(" "):
		return {"word":word,"type":"noun","class":"conjunction","tense":"present","id":"conj"}


	# Irregular verbs
	if DATA["verb-past"].get(word):
		return {"word":word,"type":"verb","class":"irregular-past","tense":"past","id":"v.i.p"}

	if DATA["verb-present"].get(word):
		return {"word":word,"type":"verb","class":"irregular-present","tense":"present","id":"v.i"}


	# Regular past tense (walked, played, studied)
	if word.endswith("ed"):
		return {"word":word,"type":"verb","class":"past","tense":"past","id":"v.p"}

	# Present tense (walks, runs, talking)
	if word.endswith(("s", "es", "ing")):
		return {"word":word,"type":"verb","class":"past","tense":"present","id":"v"}

def Syntax(value):
	
	grp = WordGroup(value)
	if not grp:
		return
	
	if grp in {"verb","noun","adverb"}:
		return
	
	return grp


def WordGroup(value):

	try:
		val = value.lower()
	except:
		return
	
	return DATA["words"].get(val)


DATA = {
	"alias":{
		"=":"equals",
		"==":"equals",
		"&":"and",
		"&&":"and",
		"|":"or",
		"||":"or"
	},    
	"types":{
		"verb":"v",
		"noun":"n",
		"adjective":"adj",    
		"pronoun":"p",
		"adverb":"adv",
		"preposition":"prep",
		"conjunction":"conj",
		"determiner":"deter",
		"interjections":"intj"
	},    
	"words":{
		"about":"preposition",
		"above":"preposition",
		"across":"preposition",
		"after":"preposition",
		"against":"preposition",
		"along":"preposition",
		"among":"preposition",
		"around":"preposition",
		"as":"preposition",
		"at":"preposition",
		"before":"preposition",
		"behind":"preposition",
		"below":"preposition",
		"beneath":"preposition",
		"beside":"preposition",
		"between":"preposition",
		"beyond":"preposition",
		"by":"preposition",
		"concerning":"preposition",
		"considering":"preposition",
		"despite":"preposition",
		"down":"preposition",
		"during":"preposition",
		"except":"preposition",
		"for":"preposition",
		"from":"preposition",
		"in":"preposition",
		"inside":"preposition",
		"into":"preposition",
		"like":"preposition",
		"near":"preposition",
		"of":"preposition",
		"off":"preposition",
		"on":"preposition",
		"onto":"preposition",
		"out":"preposition",
		"outside":"preposition",
		"over":"preposition",
		"past":"preposition",
		"regarding":"preposition",
		"round":"preposition",
		"since":"preposition",
		"through":"preposition",
		"throughout":"preposition",
		"till":"preposition",
		"to":"preposition",
		"toward":"preposition",
		"towards":"preposition",
		"under":"preposition",
		"underneath":"preposition",
		"until":"preposition",
		"up":"preposition",
		"upon":"preposition",
		"with":"preposition",
		"within":"preposition",
		"without":"preposition",
		"according to":"preposition",
		"ahead of":"preposition",
		"apart from":"preposition",
		"as for":"preposition",
		"as of":"preposition",
		"because of":"preposition",
		"by means of":"preposition",
		"close to":"preposition",
		"due to":"preposition",
		"far from":"preposition",
		"in addition to":"preposition",
		"in front of":"preposition",
		"in place of":"preposition",
		"in spite of":"preposition",
		"instead of":"preposition",
		"near to":"preposition",
		"on account of":"preposition",
		"out of":"preposition",
		"owing to":"preposition",
		"prior to":"preposition",
		"thanks to":"preposition",
		"up to":"preposition",
		"with regard to":"preposition",
		"and":"conjunction",
		"but":"conjunction",
		"or":"conjunction",
		"nor":"conjunction",
		"for":"conjunction",
		"yet":"conjunction",
		"so":"conjunction",
		"after":"conjunction",
		"although":"conjunction",
		"as":"conjunction",
		"because":"conjunction",
		"before":"conjunction",
		"if":"conjunction",
		"once":"conjunction",
		"provided":"conjunction",
		"since":"conjunction",
		"than":"conjunction",
		"though":"conjunction",
		"unless":"conjunction",
		"until":"conjunction",
		"whenever":"conjunction",
		"whereas":"conjunction",
		"wherever":"conjunction",
		"while":"conjunction",
		"even if":"conjunction-irregular",
		"even though":"conjunction-irregular",
		"in order that":"conjunction-irregular",
		"provided that":"conjunction-irregular",
		"rather than":"conjunction-irregular",
		"both * and":"conjunction-irregular",
		"either * or":"conjunction-irregular",
		"neither * nor":"conjunction-irregular",
		"not only * but also":"conjunction-irregular",
		"whether * or":"conjunction-irregular",
		"so that":"conjunction-irregular",
		"a":"determiner",
		"an":"determiner",
		"the":"determiner",
		"this":"determiner",
		"that":"determiner",
		"these":"determiner",
		"those":"determiner",
		"my":"determiner",
		"your":"determiner",
		"his":"determiner",
		"her":"determiner",
		"its":"determiner",
		"our":"determiner",
		"their":"determiner",
		"whose":"determiner",
		"all":"determiner",
		"both":"determiner",
		"each":"determiner",
		"every":"determiner",
		"either":"determiner",
		"neither":"determiner",
		"some":"determiner",
		"any":"determiner",
		"no":"determiner",
		"enough":"determiner",
		"much":"determiner",
		"many":"determiner",
		"more":"determiner",
		"most":"determiner",
		"less":"determiner",
		"least":"determiner",
		"few":"determiner",
		"fewer":"determiner",
		"fewest":"determiner",
		"little":"determiner",
		"lesser":"determiner",
		"several":"determiner",
		"such":"determiner",
		"whatever":"determiner",
		"which":"determiner",
		"whichever":"determiner",
		"another":"determiner",
		"other":"determiner",
		"same":"determiner",
		"certain":"determiner",
		"various":"determiner",
		"ah":"interjection",
		"aha":"interjection",
		"alas":"interjection",
		"aww":"interjection",
		"bah":"interjection",
		"bam":"interjection",
		"bang":"interjection",
		"behold":"interjection",
		"boo":"interjection",
		"bravo":"interjection",
		"brr":"interjection",
		"bye":"interjection",
		"cheers":"interjection",
		"damn":"interjection",
		"dang":"interjection",
		"darn":"interjection",
		"dear":"interjection",
		"eh":"interjection",
		"ek":"interjection",
		"er":"interjection",
		"ew":"interjection",
		"fie":"interjection",
		"gah":"interjection",
		"gee":"interjection",
		"gosh":"interjection",
		"ha":"interjection",
		"haha":"interjection",
		"hail":"interjection",
		"hey":"interjection",
		"hmm":"interjection",
		"ho":"interjection",
		"holy":"interjection",
		"huh":"interjection",
		"ick":"interjection",
		"indeed":"interjection",
		"lo":"interjection",
		"look":"interjection",
		"meh":"interjection",
		"mm":"interjection",
		"nah":"interjection",
		"no":"interjection",
		"oh":"interjection",
		"oh dear":"interjection",
		"oh my":"interjection",
		"oops":"interjection",
		"ouch":"interjection",
		"ow":"interjection",
		"phew":"interjection",
		"psst":"interjection",
		"rah":"interjection",
		"rats":"interjection",
		"right":"interjection",
		"shh":"interjection",
		"shoot":"interjection",
		"snap":"interjection",
		"ta":"interjection",
		"thanks":"interjection",
		"there":"interjection",
		"tsk":"interjection",
		"uh":"interjection",
		"uh-huh":"interjection",
		"uh huh":"interjection",
		"um":"interjection",
		"well":"interjection",
		"whee":"interjection",
		"whoa":"interjection",
		"wow":"interjection",
		"yeah":"interjection",
		"yes":"interjection",
		"yikes":"interjection",
		"yo":"interjection",
		"yuck":"interjection",
		"all":"pronoun",
		"another":"pronoun",
		"any":"pronoun",
		"anybody":"pronoun",
		"anyone":"pronoun",
		"anything":"pronoun",
		"both":"pronoun",
		"each":"pronoun",
		"each other":"pronoun",
		"either":"pronoun",
		"everybody":"pronoun",
		"everyone":"pronoun",
		"everything":"pronoun",
		"few":"pronoun",
		"he":"pronoun",
		"her":"pronoun",
		"hers":"pronoun",
		"herself":"pronoun",
		"him":"pronoun",
		"himself":"pronoun",
		"his":"pronoun",
		"i":"pronoun",
		"it":"pronoun",
		"its":"pronoun",
		"itself":"pronoun",
		"many":"pronoun",
		"me":"pronoun",
		"mine":"pronoun",
		"most":"pronoun",
		"my":"pronoun",
		"myself":"pronoun",
		"neither":"pronoun",
		"no one":"pronoun",
		"nobody":"pronoun",
		"none":"pronoun",
		"nothing":"pronoun",
		"one":"pronoun",
		"one another":"pronoun",
		"ours":"pronoun",
		"ourselves":"pronoun",
		"our":"pronoun",
		"she":"pronoun",
		"some":"pronoun",
		"somebody":"pronoun",
		"someone":"pronoun",
		"something":"pronoun",
		"that":"pronoun",
		"theirs":"pronoun",
		"them":"pronoun",
		"themselves":"pronoun",
		"their":"pronoun",
		"these":"pronoun",
		"they":"pronoun",
		"this":"pronoun",
		"those":"pronoun",
		"us":"pronoun",
		"we":"pronoun",
		"whatever":"pronoun",
		"which":"pronoun",
		"whichever":"pronoun",
		"who":"pronoun",
		"whoever":"pronoun",
		"whom":"pronoun",
		"whose":"pronoun",
		"you":"pronoun",
		"your":"pronoun",
		"yours":"pronoun",
		"yourself":"pronoun",
		"yourselves":"pronoun",
		"always":"adverb-fequency",
		"usually":"adverb-fequency",
		"often":"adverb-fequency",
		"regularly":"adverb-fequency",
		"occasionally":"adverb-fequency",
		"seldom":"adverb-fequency",
		"rarely":"adverb-fequency",
		"never":"adverb-fequency",
		"hardly ever":"adverb-fequency",
		"occasionally.":"adverb-fequency",
		"frequently":"adverb-fequency",
		"generally":"adverb-fequency",
		"normally":"adverb-fequency",
		"periodically":"adverb-fequency",
		"very":"adverb-degree",
		"too":"adverb-degree",
		"quite":"adverb-degree",
		"rather":"adverb-degree",
		"slightly":"adverb-degree",
		"highly":"adverb-degree",
		"partially":"adverb-degree",
		"mostly":"adverb-degree",
		"completely":"adverb-degree",
		"deeply":"adverb-degree",
		"fully":"adverb-degree",
		"hardly":"adverb-degree",
		"nearly":"adverb-degree",
		"perfectly":"adverb-degree",
		"carefully":"adverb-manner",
		"easily":"adverb-manner",
		"quickly":"adverb-manner",
		"slowly":"adverb-manner",
		"loudly":"adverb-manner",
		"softly":"adverb-manner",
		"accurately":"adverb-manner",
		"bravely":"adverb-manner",
		"cheerfully":"adverb-manner",
		"comfortably":"adverb-manner",
		"vigorously":"adverb-manner",
		"diligently":"adverb-manner",
		"effortlessly":"adverb-manner",
		"fearlessly":"adverb-manner",
		"everywhere":"adverb-place",
		"here":"adverb-place",
		"anywhere":"adverb-place",
		"anyplace":"adverb-place",
		"somewhere":"adverb-place",
		"everywhere":"adverb-place",
		"nowhere":"adverb-place",
		"abroad":"adverb-place",
		"outdoors":"adverb-place",
		"upstairs":"adverb-place",
		"downstairs":"adverb-place",
		"inside":"adverb-place",
		"underground":"adverb-place",
		"across":"adverb-place",
		"throughout":"adverb-place",
		"above":"adverb-place",
		"below":"adverb-place",
		"always":"adverb-time",
		"often":"adverb-time",
		"sometimes":"adverb-time",
		"never":"adverb-time",
		"occasionally":"adverb-time",
		"frequently":"adverb-time",
		"recently":"adverb-time",
		"soon":"adverb-time",
		"now":"adverb-time",
		"previously":"adverb-time",
		"immediately":"adverb-time",
		"eventually":"adverb-time",
		"simultaneously":"adverb-time",
		"furthermore":"adverb-conjuctive",
		"also":"adverb-conjuctive",
		"otherwise":"adverb-conjuctive",
		"moreover":"adverb-conjuctive",
		"thus":"adverb-conjuctive",
		"accordingly":"adverb-conjuctive",
		"nonetheless":"adverb-conjuctive",
		"instead":"adverb-conjuctive",
		"similarly":"adverb-conjuctive",
		"consequently":"adverb-conjuctive",
		"hence":"adverb-conjuctive",
		"therefore":"adverb-conjuctive",
		"subsequently":"adverb-conjuctive",
		"accordingly":"adverb-conjuctive",
		"where":"adverb-interogative",
		"when":"adverb-interogative",
		"why":"adverb-interogative",
		"what":"adverb-interogative",
		"how":"adverb-interogative",
		"to what extent":"adverb-interogative",
		"in what way":"adverb-interogative",
		"in which way":"adverb-interogative",
		"for what reason":"adverb-interogative",
		"went":"verb-past",
		"saw":"verb-past",
		"ate":"verb-past",
		"ran":"verb-past",
		"came":"verb-past",
		"did":"verb-past",
		"was":"verb-past",
		"were":"verb-past",
		"had":"verb-past",
		"made":"verb-past",
		"took":"verb-past",
		"got":"verb-past",
		"gave":"verb-past",
		"found":"verb-past",
		"thought":"verb-past",
		"knew":"verb-past",
		"felt":"verb-past",
		"became":"verb-past",
		"left":"verb-past",
		"put":"verb-past",
		"brought":"verb-past",
		"kept":"verb-past",
		"am":"verb-present",
		"is":"verb-present",
		"are":"verb-present",
		"have":"verb-present",
		"has":"verb-present",
		"do":"verb-present",
		"does":"verb-present",
		"go":"verb-present",
		"see":"verb-present",
		"eat":"verb-present",
		"run":"verb-present",
		"come":"verb-present",
		"make":"verb-present",
		"take":"verb-present",
		"get":"verb-present",
		"give":"verb-present",
		"feel":"verb-present",
		"know":"verb-present",
		"think":"verb-present",
		"put":"verb-present"
	}
}