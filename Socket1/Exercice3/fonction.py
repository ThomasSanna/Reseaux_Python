
def place_mark(num, mat, pos):
    mat[pos[0]][pos[1]] = 'X' if num == 1 else 'O'
    return mat

def is_ended(mat, num):
    symb = 'X' if num == 1 else 'O'
    n = len(mat)
    # vérifie lignes
    for i in range(n):
        if all(mat[i][j] == symb for j in range(n)):
            return True
    # vérifie colonnes
    for j in range(n):
        if all(mat[i][j] == symb for i in range(n)):
            return True
    # vérifie la 1ere diagonale
    if all(mat[i][i] == symb for i in range(n)):
        return True
    # vérifie la 2eme diagonale
    if all(mat[i][n-i-1] == symb for i in range(n)):
        return True
    # vérifie l'égalité : plus de case vide
    if all('-' not in ligne for ligne in mat):
        return True
    return False

def show_field(mat):
    for ligne in mat:
        print(' | '.join(ligne))
        
def check_espace_vide(mat, positionInput):
    # l'input ne sera qu'un nombre entier entre 1 et 9. 1 étant à la case (0,0), 9 la case (2,2)...
    # suivi du chiffre de gauche vers là droite et de haut vers le bas
    nPos = int(positionInput) - 1
    return mat[nPos//3][nPos%3]=='-'

def check_is_number(positionInput):
    chiffres = [i for i in range(1, 10)]
    return int(positionInput) in chiffres

# exemple : 1 donne (0,0), 2 donne (0,1), 3 donne (0,2), 4 donne(1,0), ..., 9 donne (2,2)
def input_str_to_position(positionInput):
    nPos = int(positionInput) - 1
    return((nPos//3, nPos%3)) 

# permet d'entrer une valeur de la position en vérifiant si elle respecte les valeurs demandées
def input_position(mat):
    isCorrectInput = False
    while not isCorrectInput:
        posInput = str(input("Entez une position (Entier de 1 à 9 dans une case vide) --> "))
        if not check_espace_vide(mat, posInput) or not check_is_number(posInput):
            if not check_espace_vide(mat, posInput):
                print("Erreur : il y a déjà un symbole dans la position. Retentez.")
            if not check_is_number(posInput):
                print("Erreur : problème de saisi, entrez un ENTIER entre 1 ET 9. Retentez.")
        else:
            isCorrectInput = True
    return posInput

def lancer(num, numAdv, matrice, premierCommencer, conn_s):
    while not is_ended(matrice, num) and not is_ended(matrice, numAdv):
        if premierCommencer:
            print("Votre tour...")
            posInputStr = input_position(matrice)
            posInput = input_str_to_position(posInputStr)
            matrice = place_mark(num, matrice, posInput)
            show_field(matrice)
            conn_s.sendall(bytes(posInputStr, 'utf-8'))
        
        if not is_ended(matrice, num) and not is_ended(matrice, numAdv):
            print("Tour de l'adversaire...")
            
        posInputAdvStr = conn_s.recv(1024).decode()
        if posInputAdvStr:
            posInputAdv = input_str_to_position(posInputAdvStr)
            matrice = place_mark(numAdv, matrice, posInputAdv)
            show_field(matrice)
            premierCommencer = True
            
            if is_ended(matrice, numAdv):
                print("Vous avez perdu...")
        else:
            if is_ended(matrice, num):
                print("Vous avez gagné !")
            else:
                print("Vous avez perdu...")