function incrementer(){
  ws.send("increment");
  fetch("/increment")
      .then(response => response.json())
      .then(data => document.getElementById("counter").textContent = data.counter)
}

function decrementer(){
  ws.send("decrement");
  fetch("/decrement")
      .then(response => response.json())
      .then(data => document.getElementById("counter").textContent = data.counter)
}