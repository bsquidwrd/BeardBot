import re


def get_team(message) -> str:
    try:
        regex = r"#(save|shave)"
        matches = re.finditer(regex, message, re.MULTILINE | re.IGNORECASE)
        print(matches)
        for matchNum, match in enumerate(matches, start=1):
            if match.group():
                return match.group()

    except:
        pass

    return None
