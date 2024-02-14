def occurence(tab):
    dico = {elt : 0 for elt in tab}
    for elt in tab:
        dico[elt] += 1
    return dico
        
print(occurence([1, 34, 'bou', 34, 'sois', 'bou']))