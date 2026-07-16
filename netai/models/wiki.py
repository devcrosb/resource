def Headers(content):

    if not isinstance(content,str):
        return []

    counters = [0] * 6
    headers: list[dict[str, str]] = []


    for line in content.splitlines():
        
        stripped = line.lstrip()

        # Markdown allows up to three leading spaces before a heading.
        leading_spaces = len(line) - len(stripped)
        if leading_spaces > 3:
            continue

        if not stripped.startswith("#"):
            continue

        level = 0

        while level < len(stripped) and stripped[level] == "#":
            level += 1

        if level == 0 or level > 6:
            continue

        # A space must follow the heading markers.
        if level >= len(stripped) or not stripped[level].isspace():
            continue

        title = stripped[level:].strip()

        if not title:
            continue

        # Remove optional closing heading markers.
        title = title.rstrip()

        while title.endswith("#"):
            title = title[:-1].rstrip()

        if not title:
            continue

        counters[level - 1] += 1

        # Reset all child heading counters.
        for index in range(level, len(counters)):
            counters[index] = 0

        id_depth = max(3, level)
        section_id = ".".join(
            str(value) for value in counters[:id_depth]
        )

        headers.append({
            "id": section_id,
            "title": title,
        })

    return headers
