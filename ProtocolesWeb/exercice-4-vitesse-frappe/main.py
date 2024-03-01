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


counter1 = 0 # initialisation du compteur de score du joueur 1
counter2 = 0
ws_connexion = []
isLaunched = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter1, counter2, ws_connexion, isLaunched
    await websocket.accept()
    if websocket not in ws_connexion:
      ws_connexion.append(websocket)
    while len(ws_connexion) < 2:
      print("En attente de connexion")
      await asyncio.sleep(3) # attente de 3 secondes
      # time.sleep(3) # (à ne pas faire sinon le serveur bloque olala)
    print("--- 2 joueurs sont connectés ! ---")
    player1 = ws_connexion[0]
    player2 = ws_connexion[1]
    if not isLaunched: # évite de lancer plusieurs fois la partie en même temps, très énervant
      await player1.send_text(json.dumps({"type" : "start"})) # on aurait pu faire "for conn in ws-co...."
      await player2.send_text(json.dumps({"type" : "start"}))
      isLaunched = True
    while True:
      try:
        data = await websocket.receive_text()
        data = json.loads(data)
        if data["type"] == "score": 
          if websocket == player1:
            await player2.send_text(json.dumps({"type" : "counter", "counterAdv" : data["score"]}))
          else:
            await player1.send_text(json.dumps({"type" : "counter", "counterAdv" : data["score"]}))
        elif data['type'] == "rejouer":
          for conn in ws_connexion:
            await conn.send_text(json.dumps({"type" : "rejouer"}))
          ws_connexion = [] # réinitialisation de la liste des connexions pour pouvoir refresh la page
          isLaunched = False
      except:
          break
      
    if websocket in ws_connexion:
      ws_connexion.remove(websocket)
    
app.mount("/static", StaticFiles(directory="static"), name="static")
    
if __name__ == "__main__":
    uvicorn.run('main:app') # Lancement de l'application avec uvicorn
    
# cd exercice-4-vitesse-frappe 
# uvicorn main:app --reload