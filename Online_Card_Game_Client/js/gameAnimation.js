let cardSelected=false;
let carduid;
let enemyId;
let hero
let enemy;
let cardPictures = [
	"images/cards/0.jpg",
	"images/cards/1.jpg",
	"images/cards/11.jpg",
	"images/cards/3.png",
	"images/cards/5.jpg",
	"images/cards/6.jpg",
	"images/cards/2.png",
	"images/cards/8.jpg",
	"images/cards/9.png",
	"images/cards/10.png",
	"images/cards/12.jpg"
];



window.addEventListener("load", ()=>{
	enemy = document.getElementById("enemyPicture");
	state();
})

function showCards(baliseVisee, tableau){
	document.getElementById(baliseVisee).innerHTML = "";
	let html = document.getElementById("card-template").innerHTML;

	for (var i = 0; i < tableau.length; i++) {
		let div = document.createElement("div");
		div.innerHTML = html;
		div.querySelector(".id").innerText = tableau[i].id;
		div.querySelector(".uid").innerText = tableau[i].uid;
		div.querySelector(".cost").innerText = tableau[i].cost;
		div.querySelector(".mechanics").innerText = tableau[i].mechanics;
		div.querySelector(".hp").innerText = tableau[i].hp;
		div.querySelector(".photo").src = cardPictures[tableau[i].cost];
		div.querySelector(".atk").innerText  = tableau[i].atk;
		if(baliseVisee === "playerCards"){
			div.onclick=()=>{
				let cardId = div.querySelector(".uid").innerText
				playCard(cardId);
			}
		}else if (baliseVisee === "enemyBoardCards"){
			div.onclick=()=>{
				enemyId = div.querySelector(".uid").innerText
				attack(enemyId);
				cardSelected=false;
			}
		}else if(baliseVisee === "playerBoardCards"){
			div.onclick=()=>{
				cardSelected = true;
				carduid = div.querySelector(".uid").innerText
			}
		}
		document.getElementById(baliseVisee).appendChild(div);
	}
}
function showInterface(gameState){
	document.querySelector("#remainingTime").innerText = gameState.remainingTurnTime;
	document.querySelector("#playerHp").innerText = gameState.hp;
	document.querySelector("#enemyHp").innerText = gameState.opponent.hp;
	document.querySelector("#playerGold").innerText = gameState.mp;
	document.querySelector("#enemyPicture").innerText = gameState.opponent.username;
	document.querySelector("#enemyRemainingCardsCount").innerText = gameState.opponent.remainingCardsCount;
	document.querySelector("#playerRemainingCardsCount").innerText = gameState.remainingCardsCount;

	showCards("playerCards",gameState.hand);
	showCards("playerBoardCards",gameState.board);
	showCards("enemyBoardCards",gameState.opponent.board);
}

function state() {
	$.ajax({
		url : "ajaxState.php",
		type : "POST",
		data: {
			type : "status"
		}
	})
	.done(function (msg) {
	let gameState = JSON.parse(msg);

	if(gameState == "WAITING"){
		afficherResultat("waiting");
	}else if(gameState == "LAST_GAME_WON"){
		afficherResultat("win");
	}else if(gameState == "LAST_GAME_LOST"){
		afficherResultat("lost");
	}else if(typeof gameState === "object") {
		showInterface(gameState);
	}
	else{
		console.log("statessssss");
		afficherErreurs(gameState);
	}

	if(gameState.yourTurn){
		showAvailable("endTurn");
		if(!gameState.heroPowerAlreadyUsed && gameState.mp >= 2){
			showAvailable("heroPower");
		}
	}
	setTimeout(state, 1000); // Attendre 1 seconde avant de relancer l’appel
	})
}
function showAvailable(id){
	let b = document.getElementById(id);
	b.style.backgroundColor = "#32ff7e";
	sleep(1000).then(()=>{
		b.style.backgroundColor = "initial";
	});
}
function playCard(cardId){
	$.ajax({
		url : "ajaxState.php",
		type : "POST",
		data : {
			uid : cardId,
			type : "playCard"
		}
	})
	.done(function (msg) {
		let gameState = JSON.parse(msg);


		if(typeof gameState === "object") {
			showInterface(gameState);
		}else{
			afficherErreurs(gameState);
		}
	})
}
function attack(enemyId){
	$.ajax({
		url : "ajaxState.php",
		type : "POST",
		data : {
			uid : carduid,
			targetuid : enemyId,
			type : "attack"
		}
	})
	.done(function (msg) {
		let gameState = JSON.parse(msg);


		if(typeof gameState === "object") {
			showInterface(gameState);
		}else{
			afficherErreurs(gameState);
		}
	})
}

function endTurn() {
	$.ajax({
		url : "ajaxState.php",
		type : "POST",
		data : {
			type : "endTurn"
		}
	})
	.done(function (msg) {
		let gameState = JSON.parse(msg);


		if(typeof gameState === "object") {
			showInterface(gameState);
		}else{
			afficherErreurs(gameState);
		}
	})
}

function heroPower() {
	$.ajax({
		url : "ajaxState.php",
		type : "POST",
		data : {
			type : "heroPower"
		}
	})
	.done(function (msg) {
		let gameState = JSON.parse(msg);


		if(typeof gameState === "object") {
			showInterface(gameState);
		}else {
			afficherErreurs(gameState);
		}
	})
}

function attackHero(){
	if (cardSelected){
		attack(0);
		cardSelected=false;
	}
}
function sleep (time) {
	return new Promise((resolve) => setTimeout(resolve, time));
}
function afficherErreurs(err){
	document.querySelector(".afficherErreurs h1").innerText = err;
	document.querySelector(".afficherErreurs").style.display = "initial";
	sleep(1000).then(()=>{
		document.querySelector(".afficherErreurs").style.display = "none";
	});
}
function afficherResultat(rep){

	let h1 = document.querySelector(".resultatGame h1");
	let image = document.querySelector(".photoResultat");

	if(rep === "win"){
		h1.innerText = "WIN!"
		h1.style.color="gold";
		image.src = "images/homerTourne.gif";
	}else if (rep === "lost"){
		h1.innerText = "LOST!"
		h1.style.color="red";
		image.src = "images/jesusShowOff.gif";
	}else if("waiting"){
		h1.innerText = "Waiting ..."
	}
	document.querySelector(".resultatGame").style.display = "initial";
	if(rep=== "win" || rep==="lost"){
		sleep(5000).then(()=>{
			window.location.href = "./accueil.php";
		});
	}else{
		sleep(2000).then(()=>{
			document.querySelector(".resultatGame").style.display = "none";
		});

	}
}