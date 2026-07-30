
### Parsers:
### --------------------------------------------------------------------

from netai.models.english import Word, WordType, WordGroup, Syntax, BaseWord
from netai.models.text import Text, Tokens, Labels
from netai.models.ascii import Ascii
from netai.models.encode import DF, DT, SHA1, Pop, JSON, CSV_To_DF
from netai.models.values import Int, Float, Safe,Semantic, Key
from netai.models.geo import CountryID, Country
from netai.models.ipam import Email,Domain,FQDN,Hostname,IP,Network,Mask,DNS


### Validators:
### --------------------------------------------------------------------

from netai.models.english import isWord, isWordType, isWordGroup, isSyntax, isPlural
from netai.models.text import isText
from netai.models.ascii import isAscii
from netai.models.encode import isDF, isDT, isJSON
from netai.models.values import isInt, isFloat, isSafe, isSemantic, isKey
from netai.models.geo import isCountryID, isCountry
from netai.models.ipam import isEmail, isDomain, isFQDN, isHostname, isIP, isNetwork, isMask, isDNS


### Tools
### --------------------------------------------------------------------

def SetType(key,value):

    if key == "null":
        return 

    if key == "object":
        return value

    if key == "integer":
        return Int(value)

    if key == "decimal":
        return Float(value)

    if key == "json":
        return JSON(value)
   
    if key == "key":
        return Key(value)

    if key == "word":
        return Word(value)

    if key == "hostname":
        return Hostname(value)
     
    if key == "network":
        return Network(value)
    
    if key == "dns":
        return DNS(value)

    if key == "ip":
        return IP(value)

    if key == "email":
        return Email(value)

    if key == "fqdn":
        return FQDN(value)

    if key ==  "domain":
        return Domain(value)
    
    if key == "mask":
        return Mask(value)
    
    if key == "contry_id":
        return CountryID(value)
    
    if key == "country":
        return Country(value)

    if key == "string":
        return str(value)
    
    if key == "text":
        return Text(value)

    return Ascii(value)



def GetType(value):

    if value is None:
        return "null"

    if isinstance(value,int):
        return "integer"

    if isinstance(value,float):
        return "decimal"

    if isJSON(value):
        return "json"

    if not isinstance(value,str):
        return "object"

    if len(value) == 0:
        return "null"
    
    if value.isdigit():
        return "integer"    

    if isKey(value):
        return "key"

    if isCountry(value):
        return "country"
    
    if isCountryID(value):
        return "country_id"

    if value.isalpha() and isWord(value):
        return "word"

    if not value.count("."):
        pass

    elif isNetwork(value):
        return "network"
    
    elif isDNS(value):
        return "dns"

    elif isIP(value):
        return "ip"

    elif isEmail(value):
        return "email"

    elif isFQDN(value):
        return "fqdn"

    elif isDomain(value):
        return "domain"
    
    elif value.isdecimal():
        return "decimal"    
    
    elif isSemantic(value):
        return "value"
    
    else:
        return "syntax"


    if isHostname(value):
        return "hostname"
           
    if isWord(value):
        if isSyntax(value):
            return "syntax"
        else:
            return "word"
    
    if value.isalpha():
        return "alpha"
    
    if isSemantic(value):
        return "value"
    
    return "syntax"
