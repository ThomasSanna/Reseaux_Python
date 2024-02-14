import json

f = open('Socket1\Exercice7\super-hero-squad.json', encoding='utf-8')

data = json.load(f)

class SuperHero:
    def __init__(self, name, age, secretIdentity, powers):
        self.name = name
        self.age = age
        self.secretIdentity = secretIdentity
        self.powers = powers
        
    def to_dico(self):
        return {
            'name' : self.name,
            'age' : self.age,
            'secretIdentity' : self.secretIdentity,
            'powers' : self.powers
        }
        
    def to_json(self):
        return json.dumps(self.to_dico())
    
allSuperHeros = []

for elt in data["members"]:
    allSuperHeros.append(SuperHero(elt['name'], elt['age'], elt['secretIdentity'], elt['powers']))

for elt in allSuperHeros:
    print(elt.to_dico())
    
for elt in allSuperHeros:
    print(elt.to_json())