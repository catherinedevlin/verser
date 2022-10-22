def abbrev(full: str) -> str:
    return "".join(word[0] for word in full.split() if word[0].isupper())


language_names = {"en": "English"}
