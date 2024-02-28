// Crée une instance de WebSocket
const ws = new WebSocket("ws://localhost:8000/ws");

// Gère les messages reçus du serveur WebSocket
ws.onmessage = function (event) {
  document.getElementById("counter").textContent = event.data;
};

function incrementer() {
  ws.send("increment");
}

function decrementer() {
  ws.send("decrement");
}