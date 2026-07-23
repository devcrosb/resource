from netai.display import Display
import unicodedata

def CleanText(text):

	if text is None:
		return

	vals = Split(text)

	if vals:
		return " ".join(vals)


def Split(text):

	text = str(text)

	res = []
	word = None

	for val in text:

		if val.isalnum():
			if word:
				word+=val
			else:
				word=val
		elif not word:
			pass
		elif val in {"-","."}:
			if word[-1].isalnum():
				word+=val
			else:
				res.append(StripWord(word))
				word = None
		else:
			res.append(StripWord(word))
			word = None

	if word:
		res.append(StripWord(word))

	return res

def isPunct(val):

	if len(val) != 1:
		return False

	if val in {".","?",":",";","?",","}:
		return True


def StripWord(val):

	return val.strip(".").strip("-")


def Val(val):

	if val == "*":
		return

	if val.isalnum:
		return val
	
	if val in {"-","."}:
		return val



def isSemantic(value):

	value = str(value)
	for v in value:
		if v.isalnum():
			return True
	

def Normalize(value):

	value = unicodedata.normalize("NFKC", value)
	value = value.casefold()

	if isSemantic(value):
		return value.replace(".","-")
	

def DocPath(text):

	tokens = Tokens(text)

	if tokens:
		return ".".join(tokens)


def Tokens(text):

	res = []

	for val in Split(text):
		token = Normalize(val)
		if token:
			res.append(token)

	return DeDupe(res)


def DeDupe(vals):

	return list(dict.fromkeys(vals))


def Sections(content: str) -> dict[str, str]:
	"""
	Split a Markdown document into hierarchical header/content blocks.

	Parent header names are prepended to each section header.

	Example:
		"Locations Asia Pacific Australia Sydney": "Content text 4"
	"""
	sections: dict[str, str] = {}
	header_stack: list[str] = []

	current_key: str | None = None
	content_lines: list[str] = []

	def add_section() -> None:
		if current_key is None:
			return

		content = f"{current_key}:\n" + "\n".join(content_lines).strip()

		if current_key in sections and content:
			# Preserve content if an identical hierarchical header occurs again.
			sections[current_key] = "\n\n".join(
				part for part in (sections[current_key], content) if part
			)
		else:
			sections[current_key] = content

	for line in content.splitlines():
		stripped = line.lstrip()

		# A valid ATX header starts with 1-6 hashes followed by whitespace.
		hash_count = len(stripped) - len(stripped.lstrip("#"))

		is_header = (
			1 <= hash_count <= 6
			and len(stripped) > hash_count
			and stripped[hash_count].isspace()
		)

		if is_header:
			add_section()
			content_lines = []

			header = stripped[hash_count:].strip()

			# Remove an optional closing sequence of Markdown header hashes.
			header = header.rstrip("#").rstrip()

			level_index = hash_count - 1

			# Remove headers at the current level and any deeper levels.
			header_stack = header_stack[:level_index]

			# Handle skipped levels, such as # followed directly by ###.
			while len(header_stack) < level_index:
				header_stack.append("")

			header_stack.append(header)

			current_key = " ".join(
				part for part in header_stack if part
			)

		elif current_key is not None:
			content_lines.append(line)

	add_section()

	return sections


def ReadMD(path):

	sections = Sections(open(path).read())

	data = []

	for name, content in sections.items():
		title,content = content.split(":\n",1)
		size = len(content)

		data.append({"path":DocPath(name),"title":title,"size":size,"tokens":Tokens(content),"content":content})

	return data

def main():

	data = ReadMD("scripts/test.md")

	Display(data)



if __name__ == "__main__":
	main()
	
	

