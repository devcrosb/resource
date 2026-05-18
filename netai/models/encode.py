import hashlib
import csv
import json
from io import StringIO

def Pop(rec,key):

    try:
        val = rec[key]
        del rec[key]
    except:
        val = None

    return val


def SHA1(text):

    text = str(text)

    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def isJSON(data):

    if isinstance(data,(list,dict)):
        return True
    else:
        return False    


def JSON(data):

    if data is None:
        return {}

    if isJSON(data):
        return data

    try:
        return json.loads(data)
    except:
        pass

    return {}


def isDF(data):

    if not data:
        return False

    if not isinstance(data,list):
        return False

    if not isinstance(data[0],dict):
        return False
    
    return True


def isDT(data):

    if not data:
        return False

    if not isinstance(data,list):
        return False

    if not isinstance(data[0],(list,tuple)):
        return False
    
    return True


def DF(data):

    if isCSV(data):
        return CSV_To_DF(data)

    if not isJSON(data):
        return []

    if not data:
        return []

    if isDF(data):
        return data

    if isinstance(data,dict):
        return [data]
    
    if not isDT(data):
        return []
    
    header = data[0]

    res = []

    for x in data[1:]:
        res.append(Record(x,header))

    return res


def Record(x,cols):
    
    rec = {}
    
    n = 0

    for key in cols:
        rec[key] = x[n]
        n+=1

    return rec


def DT(data):

    if isinstance(data[0],list):
        return data
    
    cols = [key for key in data[0].keys()]

    res = []
    for x in data:
        row = []
        for key in cols:
            row.append(x.get(key))
        res.append(row)

    return res


def CSV_To_DF(text):

    if not isinstance(text,str):
        return []

    """
    Convert CSV text into a list of dictionaries (JSON-ready).
    
    Args:
        csv_text (str): CSV content as a string
    
    Returns:
        list[dict]: List of rows as dictionaries
    """
    # Use StringIO so csv.DictReader can read from the string like a file
    memFile = StringIO(text)
    
    reader = csv.DictReader(memFile)
    
    # Convert each row into a dictionary
    return [row for row in reader]


def isCSV(data):
    
    if not isinstance(data,str):
        return False

    header = 0

    for line in data.split("\n"):
        if len(line) == 0:
            pass
        elif line.count(",") == 0:
            return False
        elif not header:
            header = line.count(",")
        elif line.count(",") < header:
            return False
        else:
            return True
