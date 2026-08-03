import re
import yaml
import json
from markdown import markdown as Markdown
from html import escape

### Encoder
### ===================================================================

def HTML(content):

	encoding = Detect(content)

	if encoding in {"null","value"}:
		return
	
	if encoding == "text":
		return content

	if encoding == "html":
		return content

	if encoding == "git-md":
		return GitMD_To_HTML(content)
	
	if encoding == "wiki-md":
		return WikiMD_To_HTML(content)

	if encoding == "json":
		return JSON_To_HTML(content)

	return f"<pre>{str(content)}</pre>"


def Detect(text):

	if text is None:
		return "null"
	
	if isinstance(text,(list,dict)):
		return "json"

	if not isinstance(text,str):
		return "value"

	if len(text) == 0:
		return "null"

	if text.isalnum():
		return "value"

	if isYAML(text):
		return "yaml"
	
	if isJSON(text):
		return "json"
	
	if isGitMD(text):
		return "git-md"
	
	if isWikiMD(text):
		return "wiki-md"
	
	if isHTML(text):
		return "html"
	
	return "text"
	


### Detectors
### ===================================================================


def isJSON(text):
	try:
		if isinstance(json.loads(text),(list,dict)):
			return True
	except:
		pass
	
	return False


def isYAML(text):
	try:
		if isinstance(yaml.safe_load(text),(list,dict)):
			return True
	except:
		pass
	
	return False


def isGitMD(text: str) -> bool:
	patterns = [
		r"^#{1,6}\s+",              # # Heading
		r"^\s*[-*+]\s+",            # bullets
		r"^\s*\d+\.\s+",            # numbered lists
		r"```[\s\S]*?```",          # fenced code
		r"`[^`\n]+`",               # inline code
		r"\[.+?\]\(.+?\)",          # links
		r"!\[.*?\]\(.+?\)",         # images
		r"\*\*.+?\*\*",             # bold
		r"^\|.*\|$",                # tables
		r"^>\s+",                   # blockquotes
	]
	return InPattern(text, patterns)


def isWikiMD(text: str) -> bool:
	patterns = [
		r"^={1,6}[^=\n].*?={1,6}$", # == Heading ==
		r"\[\[.+?\]\]",             # [[Page]]
		r"\{\{.+?\}\}",             # {{Template}}
		r"^\{\|",                   # MediaWiki table start
		r"^\|\}",                   # MediaWiki table end
		r"^\|[-+]",                 # table rows
		r"^!.*",                    # table headers
	]
	return InPattern(text, patterns)


def isConfluenceMD(text: str) -> bool:
	patterns = [
		r"^h[1-6]\.\s+",            # h1. Heading
		r"\|\|.*\|\|",              # table headers
		r"\{code(:.*?)?\}",         # {code}
		r"\{panel(:.*?)?\}",        # {panel}
		r"\{quote\}",               # {quote}
		r"\[.+?\|.+?\]",            # [label|url]
	]
	return InPattern(text, patterns)


def isAsciiDoc(text: str) -> bool:
	patterns = [
		r"^=\s+.+$",                # = Title
		r"^==+\s+.+$",              # == Section
		r"^\[source.*?\]$",         # [source,python]
		r"^----$",                  # code fence
		r"^include::.+?\[\]",        # include::file[]
		r"^image::.+?\[.*?\]",       # image::file[]
		r"^ifdef::.+?\[\]",          # ifdef::name[]
	]
	return InPattern(text, patterns)


def isHTML(text: str) -> bool:

	ld = text.count("<")
	rd = text.count(">")

	if (ld < 2) or (rd < 2):
		return False

	patterns = [
		r"<!DOCTYPE\s+html",
		r"<html\b[^>]*>",
		r"</html>",
		r"<head\b[^>]*>",
		r"<body\b[^>]*>",
		r"<div\b[^>]*>",
		r"<span\b[^>]*>",
		r"<p\b[^>]*>",
		r"<a\b[^>]*>",
		r"<table\b[^>]*>",
		r"<h[1-6]\b[^>]*>",
		r"<ul\b[^>]*>",
		r"<ol\b[^>]*>",
		r"<li\b[^>]*>",
		r"<img\b[^>]*>",
		r"<br\s*/?>",
	]

	return InPattern(text, patterns)

### JSON Encoders:
### ===================================================================


def Text_to_JSON(text):

	try:
		return json.loads(text)
	except:
		pass


def YAML_to_JSON(text):
	try:
		return yaml.safe_load(text)
	except:
		pass

def GitMD_to_JSON(text):

	return text

def WikiMD_to_JSON(text):

	return text


### HTML Encoders:
### ===================================================================

def JSON_To_HTML(data):
	
	if isinstance(data,str):
		try:
			data = json.loads(data)
		except:
			data = {"content":str(data)}

	try:
		data = json.dumps(data,indent=4)
	except:
		data = str(data)

	return f"<pre>{data}</pre>"



def GitMD_To_HTML(text):

	if not isinstance(text,str):
		return ""

	try: 
		html = Markdown(text,
			extensions=[
				"extra",
				"tables",
				"fenced_code",
				"toc",
				"sane_lists",
			])
	except:
		html = f"<pre>GitMD:\n{text}</pre>"

	return html


def WikiMD_To_HTML(text):

	if not isinstance(text,str):
		return ""
	
	try: 
		html = escape(text)
	except:
		return f"<pre>WikiMD:\n{text}</pre>"

	# Headings: == Heading ==
	html = re.sub(
		r"^={6}\s*(.*?)\s*={6}$",
		r"<h6>\1</h6>",
		html,
		flags=re.MULTILINE)
	
	html = re.sub(r"^={5}\s*(.*?)\s*={5}$", r"<h5>\1</h5>", html, flags=re.MULTILINE)
	html = re.sub(r"^={4}\s*(.*?)\s*={4}$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
	html = re.sub(r"^={3}\s*(.*?)\s*={3}$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
	html = re.sub(r"^={2}\s*(.*?)\s*={2}$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
	html = re.sub(r"^={1}\s*(.*?)\s*={1}$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

	# Bold / italic
	html = re.sub(r"'''(.*?)'''", r"<strong>\1</strong>", html)
	html = re.sub(r"''(.*?)''", r"<em>\1</em>", html)

	# Internal links: [[Page]] or [[Page|Label]]
	html = re.sub(
		r"\[\[([^|\]]+)\|([^\]]+)\]\]",
		r'<a href="\1">\2</a>',
		html,
	)
	html = re.sub(
		r"\[\[([^\]]+)\]\]",
		r'<a href="\1">\1</a>',
		html,
	)

	# External links: [https://example.com Label]
	html = re.sub(
		r"\[(https?://[^\s\]]+)\s+([^\]]+)\]",
		r'<a href="\1">\2</a>',
		html,
	)

	# Very simple paragraph handling
	blocks = html.split("\n\n")
	rendered_blocks = []

	for block in blocks:
		block = block.strip()

		if not block:
			continue

		if re.match(r"^<h[1-6]>.*</h[1-6]>$", block):
			rendered_blocks.append(block)
		else:
			block = block.replace("\n", "<br>\n")
			rendered_blocks.append(f"<p>{block}</p>")

	return "\n".join(rendered_blocks)


def DF_to_WikiMD(rows):

    if not rows:
        return '{| class="wikitable"\n|}'


    columns = list(rows[0].keys())

    def format_value(value: Any) -> str:
        if value is None:
            return ""

        # Keep each table cell on one line.
        return str(value).replace("\r\n", "<br>").replace("\n", "<br>")

    lines = [
        '{| class="wikitable"',
        "|-",
        "! " + " !! ".join(format_value(column) for column in columns),
    ]

    for row in rows:
        lines.append("|-")
        lines.append(
            "| " + " || ".join(
                format_value(row.get(column, ""))
                for column in columns
            )
        )

    lines.append("|}")
    return "\n".join(lines)	


### Helpers
### ===================================================================


def InPattern(text: str, patterns: list[str]) -> bool:
	return any(re.search(pattern, text, re.MULTILINE | re.IGNORECASE) for pattern in patterns)


