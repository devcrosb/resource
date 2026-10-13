from netai.models.ascii import Ascii, isAscii
import re



def Tokens(text,n=1):

    res = {}

    text = text.replace("\r","")
    text = text.replace("-\n"," ")

    for line in text.split("\n"):
        
        for val in Labels(line):
            res[val] = (res.get(val) or 0) + n

    return res


def Labels(line):
    
    line = line.lower()
    line = line.replace('"'," ")

    res = []
    for val in line.split(" "):
        val = Label(val)
        if val:
            res.append(val)
    
    return res


def Label(val):

    val = Ascii(val)
    
    if not val:
        return
    
    val = str(val)

    val = val.lower().strip()
    val = RStrip(val)
    val = LStrip(val)

    if isLabel(val):
        return val


def RStrip(val):
    
    if len(val) < 1:
        return val
    
    elif val[-1].isalnum():
        return val
    
    else:
        return val[:-1]

def LStrip(val):

    if len(val) < 1:
        return val
    
    elif val[0].isalnum():
        return val
    
    else:
        return val[0]


def isLabel(val):
    
    if not isinstance(val,str):
        return False

    val = val.replace("-","")

    if len(val) == 0:
        return False
    
    if val.isalnum():
        return True

    if val.endswith("'s"):
        val = val.rsplit("'",1)[0]
        if val.isalnum():
            return True

    return False


def Text(value):
    
    if value == None:
        return
    
    res = str(value)

    res = res.strip()
 
    if len(res) > 0:
        return res
 
def isText(value):

    if Text(value):
        return True
    else:
        return False

def Match(pattern: str, text: str) -> bool:

    if not text:
        return False
    
    if not pattern:
        return True

    text = str(text)

    if "*" not in pattern:
        return text == pattern

    parts = pattern.split("*")
    pos = 0
    end = len(text)

    # Check required prefix
    if parts[0]:
        if not text.startswith(parts[0]):
            return False
        pos = len(parts[0])

    # Check required suffix
    if parts[-1]:
        if not text.endswith(parts[-1]):
            return False
        end -= len(parts[-1])

    # Find intermediate substrings in order
    for part in parts[1:-1]:
        if part:
            index = text.find(part, pos, end)
            if index == -1:
                return False
            pos = index + len(part)

    return pos <= end