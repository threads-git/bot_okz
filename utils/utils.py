import re
def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    # match = re.search(r'\b(300|[1-2]?[0-9]{1,2}|[1-9])[A-Ca-cА-Га-г]\b', text)
    if match:
        # return int(match.group(1))
        return match.group(1)
    else:
        return None

def extract_phone(text):
    # match = re.search(r'^\+?[1-9]\d{1,14}$', text)
    match = re.findall(r'\+7\d{10}', text)
    # match = re.findall(r'^((8|\+7)[\- ]?)?(\(?\d{3,4}\)?[\- ]?)?[\d\- ]{5,10}$', text)
    if match:
        if len(match[0]) == 12:
        # return int(match.group(1))
            return match
        else:
            return None
    else:
        return None