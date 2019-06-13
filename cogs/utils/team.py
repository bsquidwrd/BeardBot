import re


def get_team(message) -> str:
    regex = r"#(save|shave)"
    matches = re.finditer(regex, message, re.MULTILINE | re.IGNORECASE)

    for matchNum, match in enumerate(matches, start=1):
        if match.group():
            return match.group()
    return None
