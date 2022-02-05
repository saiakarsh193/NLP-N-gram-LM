import re

def tokenize(text):
    # substitution
    text = re.sub(r"(https?:\/|www\.)[^\(\) ]*", "<URL>", text, 0, re.MULTILINE)
    text = re.sub(r"#[^# ]+", "<HASHTAG>", text, 0, re.MULTILINE)
    text = re.sub(r"@[^@: ]+", "<MENTION>", text, 0, re.MULTILINE)

    text = re.sub(r"\*[A-Za-z ]+\*", "<ACTION>", text, 0, re.MULTILINE)
    text = re.sub(r"((\+\+?)?\d{2,4}[.-])?\d{2,4}[.-]\d{3,4}[.-]\d{3,5}", "<PHONE>", text, 0, re.MULTILINE)
    text = re.sub(r";-?\)+|:-?\)+|:-?\(+|\):|:-?p+|(&lt;|<)3|:-?D|[xX][dD]+", "<EMOTICON>", text, 0, re.MULTILINE)
    text = re.sub(r"[₹$€£₩¥] ?[\d,.]+", "<CURRENCY>", text, 0, re.MULTILINE)
    text = re.sub(r"\d+ ?%", "<PERCENTAGE>", text, 0, re.MULTILINE)
    text = re.sub(r"\d{1,2}[\/.-]\d{1,2}[\/.-]\d{1,2}", "<DATE>", text, 0, re.MULTILINE)
    text = re.sub(r"brb|lmao+|lo+l", "<ABBREVIATION>", text, 0, re.MULTILINE | re.IGNORECASE)

    # remove repeatitions
    text = re.sub(r"[.]{2,}", ",", text, 0, re.MULTILINE)
    text = re.sub(r"([^a-zA-Z0-9])(?=\1)", "", text, 0, re.MULTILINE)

    repfun = lambda x: x.group()[0] if x.group is not None else ""
    text = re.sub(r"([A-Za-z])\1{2,}", repfun, text, 0, re.MULTILINE)

    # handle punctuations
    punfun = lambda x: " " + x.group() + " " if x.group is not None else ""
    text = re.sub(r"((?=[^<>-])\W)", punfun, text, 0, re.MULTILINE)

    return text.split()

if __name__ == "__main__":
    print(tokenize("This is awesome!!! #party"))