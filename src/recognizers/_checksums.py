def luhn_check_digit(partial: str) -> int:
    digits = [int(c) for c in partial if c.isdigit()]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - (total % 10)) % 10


def luhn_valid(value: str) -> bool:
    digits = [int(c) for c in value if c.isdigit()]
    if len(digits) < 2:
        return False
    partial = value[:-1]
    return luhn_check_digit(partial) == int(value[-1])


def mod97(numeric_str: str) -> int:
    chars = []
    for ch in numeric_str:
        if ch.isdigit():
            chars.append(ch)
        else:
            chars.append(str(ord(ch.upper()) - 55))
    s = "".join(chars)
    rem = 0
    for ch in s:
        rem = ((rem * 10) + int(ch)) % 97
    return rem


def is_valid_iban(iban: str) -> bool:
    cleaned = iban.replace(" ", "").upper()
    if not cleaned.startswith("DZ"):
        return False
    if len(cleaned) != 24:
        return False
    bban = cleaned[4:]
    if not bban.isdigit() or len(bban) != 20:
        return False
    rearranged = cleaned[4:] + cleaned[:4]
    return mod97(rearranged) == 1


def is_valid_rib(rib: str) -> bool:
    cleaned = rib.replace(" ", "")
    if not cleaned.isdigit() or len(cleaned) != 20:
        return False
    return mod97(cleaned) == 0


def is_valid_luhn_nin(nin: str) -> bool:
    cleaned = nin.replace(" ", "")
    if not cleaned.isdigit() or len(cleaned) != 18:
        return False
    return luhn_valid(cleaned)
