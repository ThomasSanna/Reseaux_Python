dicoLettres = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
    'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
    'k': 10, 'l': 1, 'm': 2, 'n': 1, 'o': 1,
    'p': 3, 'q': 8, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 10, 'x': 10, 'y': 10,
    'z': 10
}

multi_bc = 2
multi_bf = 3
multi_ros = 2
multi_rou = 3


dicoDonnees = {
    "mot" : 'arbre',
    "bc" : [multi_bc, ['a']], # bleu clair : [multiplicité, liste de lettres sur la case à multiplier]
    "bf" : [multi_bf, ['e']],
    "ros" : [multi_ros, True], # True : multiplier le compte total par la multiplicité
    "rou" : [multi_rou, False]
}

def scrabble(dicoLettres=dicoLettres, dicoDonnees=dicoDonnees):
    valuesTab = list(dicoDonnees.values())
    print(valuesTab)
    
    mot = valuesTab[0].lower()
    
    count = 0
    
    for lettre in mot:
        count += dicoLettres[lettre]
        
    for i in range(1, 3):
        for elt in valuesTab[i][1]:
            if elt.lower() in mot :
                count += dicoLettres[elt.lower()] * valuesTab[i][0]-1
    
    for i in range(3, 5):
        if valuesTab[i][1]:
            count *= valuesTab[i][0]
    
    return count

print(scrabble())