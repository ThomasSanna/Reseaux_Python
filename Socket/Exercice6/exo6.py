import json

f = open('Socket1\Exercice6\departements-region.json', encoding='utf-8')

data = json.load(f)

# tabRegion = {elt["region_name"] : [dep["num_dep"] for dep in data if dep["region_name"] == elt["region_name"]] for elt in data}

tabRegion = {elt["region_name"] : [] for elt in data}

for elt2 in data:
    tabRegion[elt2["region_name"]].append(elt2["num_dep"])

print(tabRegion)






f.close()