from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI() # Création de l'application FastAPI


counter = 0 # initialisation du compteur
ws_connexion = []

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


# Polling sans websocket
@app.get("/actualisation")
def actualisation():
    return {"counter": counter}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_connexion.append(websocket)
    global counter
    while True:
        data = await websocket.receive_text()
        if data == "increment":
            counter += 1
        elif data == "decrement":
            counter -= 1
        for conn in ws_connexion:
            await conn.send_text(f"{counter}")
    
# uvicorn main:app --reload

app.mount("/static", StaticFiles(directory="static"), name="static") # Montage du dossier static

# if __name__ == '__main__':
#     uvicorn.run('main:app')