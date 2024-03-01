const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = function (event) {
  let json = JSON.parse(event.data)
  if (json.type == "counter"){
    document.querySelector('#scoreAdv').innerHTML = json.counterAdv
  }
  else if (json.type == "start"){
    launchGame()
  }
  else if (json.type == 'rejouer'){
    window.location.reload()
  }
};

function rejouer(){
  ws.send(JSON.stringify({type: "rejouer"}))
}

let scoreJou = 0
let erreurJou = 0
let indexTexte = 0
let motWin = []
let motLost = []
let texteArr = []
let texte = ""

function launchGame(){
  document.querySelector('.messageAttente').style.display = 'none'

  let start = 4
  document.querySelector('.startC').innerHTML = "Joueur trouvé !"
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
          clearInterval(chronoInterval)
          document.querySelector('.chrono').innerHTML = ""
          document.querySelector('#texteEntrer').style.display = 'none'
          document.querySelector('#texteEntrer').value = ""
          document.querySelector('.btnRejouer').style.display = 'block'
        }
      }, 1000);
    }
  }, 1000);
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
      scoreJou++
      document.querySelector('#scoreJou').innerHTML = scoreJou
    } else {
      motLost.push(indexTexte)
      erreurJou++
    }
    ws.send(JSON.stringify({type: "score", score: scoreJou}))
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

