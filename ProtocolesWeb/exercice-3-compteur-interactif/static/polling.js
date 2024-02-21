// Polling : faire une requete toutes les 5 secondes
function actualiser(){
  fetch("/actualisation")
      .then(response => response.json())
      .then(data => document.getElementById("counter").textContent = data.counter)
}

// setInterval(actualiser, 5000)