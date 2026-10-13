
from netai.models.text import inPattern, Router
import time


PATTERNS = {
    "* summarise * and then *": "summarize-then",
    "select * from *": "select-from",
    "open * and then *": "open-then",
    "open * then *": "open-then",
    "view * encoding html": "view-html",
    "view * html": "view-html",
    "* view *": "view"
}

TEST_VALS = {
    "please summarise this report and then email it": "summarize-then",
    "select name from customers": "select-from",
    "open report and then print it": "open-then",
    "open report then print it": "open-then",
    "view report encoding html": "view-html",
    "view report html": "view-html",
    "please view the report": "view",
    "unrecognised command": None
}


def GetPattern(text):

    for pattern,label in PATTERNS.items():
        if inPattern(pattern,text):
            return label

def Test1():

    start = time.perf_counter()

    print("\n Test 1:\n")

    for text, label1 in TEST_VALS.items():
        
        label2 = GetPattern(text)

        if str(label2) == str(label1):
            status = "PASS"
        else:
            status = "FAIL"

        print(f" {text} | {label1} | {status}")

    duration = round((time.perf_counter() - start) * 1000000,2)

    print(f"\n Run-Time: {duration} uSec\n")

    return duration


def Test2():

    start = time.perf_counter()

    # Prepare once; reuse for every request.
    route = Router(PATTERNS)

    print("\n Test 2:\n")

    for text, label in TEST_VALS.items():
        
        if route(text) == label:
            status = "PASS"
        else:
            status = "FAIL"

        print(f" {text} | {label} | {status}")


    duration = round((time.perf_counter() - start) * 1000000,2)

    print(f"\n Run-Time: {duration} uSec \n")

    return duration



def main():

    ts2 = Test2()
    ts1 = Test1()
    
    if ts1 < ts2:
        delta = ts2 - ts1
        winner = "Method 1"
    else:
        delta = ts1 - ts2
        winner = "Method 2"


    delta = round(delta,2)

    print(f"\n Winner-Winner-Chicken-Dinner: {winner} | Delta: {delta} uSec\n")


if __name__ == "__main__":
    main()
