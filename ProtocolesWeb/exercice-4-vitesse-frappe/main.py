from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI() # Création de l'application FastAPI


counter1 = 0 # initialisation du compteur de score du joueur 1
counter2 = 0
ws_connexion = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if len(ws_connexion) < 2:
      ws_connexion.append(websocket)
      if len(ws_connexion) == 2:
        global counter1
        global counter2
        while True:
            try:
                data = await websocket.receive_text()
                for conn in ws_connexion:
                    await conn.send_text()
            except:
                break
    else:
      await websocket.send_text("La partie est déjà en cours")
      await websocket.close()
      return
    ws_connexion.remove(websocket)
    
app.mount("/static", StaticFiles(directory="static"), name="static") # Montage du dossier static
    