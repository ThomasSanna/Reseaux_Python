from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI() # Création de l'application FastAPI

app.mount("/static", StaticFiles(directory="static"), name="static") # Montage du dossier static =

counter = 0 # Initialisation du compteur

@app.get("/") # Définition de la route
async def read_root(): # Définition de la fonction associée à la route  
    return FileResponse('static/index.html') # Retourne le fichier index.html

@app.get("/increment")
async def increment_counter():
    global counter
    counter += 1 # Incrémentation de la variable counter
    return {"counter": counter} # Retourne la valeur de counter

@app.get("/decrement") 
async def decrement_counter():
    global counter
    counter -= 1
    return {"counter": counter}

# uvicorn main:app --reload