const ws = new WebSocket("ws://localhost:8000/ws");

let indexTexte = 0
let motWin = []
let motLost = []
let texteArr = []
let texte = ""

let numJouConn = []

ws.onmessage = function (event) {
  let json = JSON.parse(event.data)

  if(json.type == "numToi"){
    autreJoueurAvant(json.numToi, json.listDeco)
  } 
  else if(json.type == "nvJoueur"){
    nouveauJoueur(json.nvJoueur)
  } 
  else if (json.type == "lancerPartie"){
    launchGame()  
  } 
  else if (json.type == "rejouer"){
    window.location.reload()
  } 
  else if (json.type == "addScore"){
    document.querySelector('#scoreJou'+json.id).innerHTML = json.score
  }
  else if (json.type == "envoieCounterFinal"){
    finPartie(json.counterTrie, json.ind)
  }
  else if (json.type == 'supprJoueur'){
    supprimerDivJou(json.supprJoueur)
  }
};

function supprimerDivJou(id){
  document.querySelector('.divJou'+id).remove()
}  


function autreJoueurAvant(numToi, listDeco){
  for (let i = 1; i <= numToi; i++){
    numJouConn.push(i)
  }
  divAdv = document.querySelector('.adversaire')
  divAdv.innerHTML = ""
  for(let i = 1; i < numToi; i++){
    if(i != numToi && !(listDeco.includes(i))){
      divAdv.innerHTML += `<div class="divJou${i}">
                             <span id="jou${i}">Joueur ${i} : </span><span class='scoreJou' id="scoreJou${i}">0</span>
                           </div>`
    }
  }
  divJou = document.querySelector('.toi')
  divJou.innerHTML = `<div class="divJou${numToi}">
                       <span id="jou${numToi}">Vous (Joueur ${numToi}) : </span><span id="scoreJou${numToi}">0</span>
                     </div>`
}

function nouveauJoueur(nvJoueur){
  if(!numJouConn.includes(nvJoueur)){
    numJouConn.push(nvJoueur)

    divAdv = document.querySelector('.adversaire')
    divAdv.innerHTML += `<div class="divJou${nvJoueur}">
                          <span id="jou${nvJoueur}">Joueur ${nvJoueur} : </span><span class='scoreJou' id="scoreJou${nvJoueur}">0</span>
                        </div>`
  }
}

function lancerPartie(){
  ws.send(JSON.stringify({type: "lancerPartie"}))
}

function rejouer(){
  ws.send(JSON.stringify({type: "rejouer"}))
}

function launchGame(){
  document.querySelector('.btnCommencer').style.display = 'none'

  let start = 4
  document.querySelector('.startC').innerHTML = "Lancement de la partie..."
  let startInterval = setInterval(() => {
    document.querySelector('.startC').innerHTML = start==4 ? "Prêt ?" : start
    start--
    if(start < 0){
      clearInterval(startInterval)
      document.querySelector('.startC').innerHTML = ""
      document.querySelector('#texteEntrer').style.display = 'block'
      document.querySelector('#texteEntrer').focus()

      let chrono = 29
      document.querySelector('.chrono').innerHTML = 30
      let chronoInterval = setInterval(() => {
        document.querySelector('.chrono').innerHTML = chrono<-1 ? 0 : chrono
        chrono--
        if(chrono < -1){
          ws.send(JSON.stringify({type: "finPartie"})) // Tous les joueurs envoient ce message en même temps
          clearInterval(chronoInterval)
        }
      }, 1000);
    }
  }, 1000);
}

function finPartie(listeTrie, ind){
  document.querySelector('.chrono').innerHTML = ""
  document.querySelector('#texteEntrer').style.display = 'none'
  document.querySelector('#texteEntrer').value = ""
  document.querySelector('.finPartie').style.display = 'flex'
  document.querySelector('.btnPage').style.display = 'flex'

  let message = ""
  let divScoresFin = document.querySelector('.scoresFin')

  valTrie = Object.values(listeTrie)

  if(valTrie[0] == listeTrie[ind]){
    message = "Bravo vous avez gagné !"
  } else {
    message = "Dommage vous avez perdu !"
  }
  document.querySelector('.messageFin').innerHTML = message

  for (let cle in listeTrie){
    let score = listeTrie[cle]
    if (score >= 0){ // Les joueurs déconnectés ont un score de -1
      divScoresFin.innerHTML += `<div class="scoreFin${parseInt(cle)+1}"> Joueur ${parseInt(cle)+1} : ${score} point(s) </div>`
    }
  }
}

function arrToString(arr){
  return arr.join(' ')
}

function stringToArr(str){
  return str.split(' ')
}

function randomText(){ // récupère un texte aléatoire avec un fichier json de plusieurs mots français trouvé sur github (https://github.com/nmondon/mots-frequents)
  fetch("./static/frequence.json")
    .then(response => response.json())
    .then(data => {
      nbMots = Math.floor(Math.random() * 20) + 30 // entre 30 et 50 mots
      for(let i = 0; i < nbMots; i++){
        let mot = data[Math.floor(Math.random() * data.length)].label
        texteArr.push(mot)
      }
      texte = arrToString(texteArr)
      affichageTexte()
    })
}

function taptap(){ // à chaque fois que l'utilisateur appuie sur une touche
  if(event.key == ' ' || event.key == 'Enter'){
    let texteEntrer = document.querySelector('#texteEntrer')
    if(texteEntrer.value.split(' ')[0] == texteArr[indexTexte]){
      motWin.push(indexTexte)
      ws.send(JSON.stringify({type: "addScore"}))
    } else {
      motLost.push(indexTexte)
    }
    indexTexte++
    texteEntrer.value = ""
    affichageTexte()
  }
}

function affichageTexte(){
  let textePlacer = document.querySelector('#textePlacer')
  let textePlacerArr = []
  for(let i = Math.floor(indexTexte/5)*5; i < texteArr.length; i++){
    if(motWin.includes(i)){
      textePlacerArr.push(`<span class='surligneVert'>${texteArr[i]}</span>`)
    } else if(motLost.includes(i)){
      textePlacerArr.push(`<span class='surligneRouge'>${texteArr[i]}</span>`)
    } else if (i == indexTexte){
      textePlacerArr.push(`<span class='enBorder'>${texteArr[i]}</span>`)
    } else{
      textePlacerArr.push(`<span>${texteArr[i]}</span>`)
    }
  }
  textePlacer.innerHTML = arrToString(textePlacerArr)
}

function closeFinPartie(){
  document.querySelector('.finPartie').style.display = 'none'
}