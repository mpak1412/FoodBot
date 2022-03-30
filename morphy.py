import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def morphy(message):
    for word in message:
        ingr_lst = []
        word = morph.parse(word)[0].normal_form
        ingr_lst.append(word)
        return ingr_lst
