import string


def chastota(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    result = {}
    for word in text.split():
        word = word.lower().strip(string.punctuation + "«»—…")
        if word:
            result[word] = result.get(word, 0) + 1
    return result
