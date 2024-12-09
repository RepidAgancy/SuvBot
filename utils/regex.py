import re

def match_phone_number(phone):
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    return bool(re.match(pattern, phone))
