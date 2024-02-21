from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI() # Création de l'application FastAPI

app.mount("/static", StaticFiles(directory="static"), name="static") # Montage du dossier static =

counter = 0 # initialisation du compteur

@app.get("/") # définition de la route
def read_root(): # définition de la fonction associée à la route  
    return FileResponse('static/index.html') # retourne le fichier index.html

@app.get("/increment")
def increment_counter():
    global counter
    counter += 1 # incrémentation de la variable counter
    return {"counter": counter} # retourne la valeur de counter

@app.get("/decrement") 
# async def....
def decrement_counter():
    global counter
    counter -= 1
    return {"counter": counter}

@app.get("/actualisation")
def actualisation():
    return {"counter": counter}

# uvicorn main:app --reload

if __name__ == '__main__':
    uvicorn.run('main:app')