from netai.models.ascii import Ascii, isAscii
from collections.abc import Callable, Mapping
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


def inPattern(pattern: str, text: str) -> bool:

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


def Router(
    patterns: Mapping[str, str],
) -> Callable[[str], str | None]:
    """Return a function that maps text to the first matching pattern's label.

    Matching is case-sensitive and covers the entire string.
    '*' matches zero or more characters, including newlines.
    An empty pattern matches any string.
    All other characters, including spaces, are literal.
    """
    rules = []

    for pattern, label in patterns.items():
        if not isinstance(pattern, str) or not isinstance(label, str):
            raise TypeError("Pattern keys and labels must be strings")

        chunks = (pattern or "*").split("*")
        prefix = chunks[0]

        if len(chunks) == 1:
            # None distinguishes exact matching from wildcard matching.
            suffix, middle = "", None
        else:
            suffix = chunks[-1]
            middle = tuple(part for part in chunks[1:-1] if part)

        minimum_length = sum(map(len, chunks))
        rules.append((prefix, suffix, middle, minimum_length, label))

    # Group rules by their required first character.
    # Unanchored patterns remain eligible in every group.
    # Original pattern order is preserved within each group.
    fallback = tuple(rule for rule in rules if not rule[0])
    first_chars = {rule[0][0] for rule in rules if rule[0]}

    buckets = {
        char: tuple(
            rule for rule in rules
            if not rule[0] or rule[0][0] == char
        )
        for char in first_chars
    }

    def match(text: str) -> str | None:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        length = len(text)
        candidates = buckets.get(text[:1], fallback)

        for prefix, suffix, middle, minimum_length, label in candidates:
            if length < minimum_length:
                continue

            if middle is None:
                if text == prefix:
                    return label
                continue

            if prefix and not text.startswith(prefix):
                continue

            if suffix and not text.endswith(suffix):
                continue

            # Reserve the suffix: separate literal segments cannot overlap.
            position = len(prefix)
            end = length - len(suffix)

            for part in middle:
                index = text.find(part, position, end)
                if index < 0:
                    break
                position = index + len(part)
            else:
                return label

        return None

    return match