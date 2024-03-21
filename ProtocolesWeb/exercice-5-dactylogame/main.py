from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import asyncio

app = FastAPI() # Création de l'application FastAPI

@app.get("/") # définition de la route
def read_root(): # définition de la fonction associée à la route
    return FileResponse('static/index.html') # retourne le fichier index.html

counter = []
ws_connexion = []
ws_status = [] # True = connecté, False = déconnecté. Nous permet d'éviter les erreurs lors d'envoi de message à des clients déconnectés
isLaunched = False

async def lancerPartie(ws_connexion):
  global isLaunched
  if not isLaunched:
    isLaunched = True
    for ws in ws_connexion:
      if ws_status[ws_connexion.index(ws)]:
        await ws.send_text(json.dumps({"type" : "lancerPartie"}))

def rejouer():
  global counter, isLaunched
  counter = []
  isLaunched = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter, ws_connexion, isLaunched
    await websocket.accept()
    if websocket not in ws_connexion:
      counter.append(0)
      ws_connexion.append(websocket)
      ws_status.append(True)
      listDeco = [i+1 for i in range(len(ws_connexion)) if not ws_status[i]]
      await websocket.send_text(json.dumps({"type" : "numToi", "numToi" : ws_connexion.index(websocket)+1, "listDeco" : listDeco}))
      for ws in ws_connexion[:-1]:
        if ws_status[ws_connexion.index(ws)]:
          await ws.send_text(json.dumps({"type" : "nvJoueur", "nvJoueur" : len(ws_connexion)}))
        
    while True:
      try:
        data = await websocket.receive_text()
        data = json.loads(data)
        
        if(data["type"] == "lancerPartie"):
          await lancerPartie(ws_connexion)
          
        elif (data["type"] == "rejouer"):
          rejouer()
          for ws in ws_connexion:
            if ws_status[ws_connexion.index(ws)]:
              await ws.send_text(json.dumps({"type" : "rejouer"}))
          ws_connexion = []
          break
          
        elif (data["type"] == "addScore"):
          indexJ = ws_connexion.index(websocket)
          counter[indexJ] += 1
          for ws in ws_connexion:
            if ws_status[ws_connexion.index(ws)]:
              await ws.send_text(json.dumps({"type" : "addScore", "score" : counter[indexJ], 'id' : indexJ+1}))
        
        elif (data["type"] == "finPartie"):
          counterTrie = sorted(counter, reverse=True)
          counterDicoTrie = { i : counterTrie[i] for i in range(len(counter))}
          await websocket.send_text(json.dumps({"type" : "envoieCounterFinal", 'counterTrie' : counterDicoTrie, 'ind' : ws_connexion.index(websocket)}))
        
      except:
          break
      
    if websocket in ws_connexion:
      ws_status[ws_connexion.index(websocket)] = False
      counter[ws_connexion.index(websocket)] = -1
      for ws in ws_connexion:
        if ws_status[ws_connexion.index(ws)]:
          await ws.send_text(json.dumps({"type" : "supprJoueur", "supprJoueur" : ws_connexion.index(websocket)+1}))
      
    
app.mount("/static", StaticFiles(directory="static"), name="static")
    
if __name__ == '__main__':
    uvicorn.run('main:app', host='172.21.3.161', port=8000)

    
# cd exercice-5-dactylogame
# uvicorn main:app --reload

