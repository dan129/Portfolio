<?php
	require_once("action/GameAction.php");

	$action = new GameAction();
	$action->execute();
?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<script type="text/javascript" src="js/jquery.min.js"></script>
	<script src="js/gameAnimation.js"></script>
	<link rel="stylesheet" href="css/game.css">
	<title>Document</title>
</head>
<body>
	<div class = 'afficherErreurs'><h1></h1></div>
	<div class = 'resultatGame'>
		<h1></h1>
		<img class = 'photoResultat' src="" alt="">
	</div>
	<template id="card-template">
		<div class='card'>
			<div class='id'></div>
			<div class='uid'></div>
			<div class='cost'></div>
			<img class = "photo" src="" alt="">
			<div class='mechanics'></div>
			<div id = "basCarte">
				<div class='atk'></div>
				<div class='hp'></div>
			</div>
		</div>
	</template>

	<div id="enemy">
		<iframe
			src="https://magix.apps-de-cours.com/server/#/chat/<?= $_SESSION["key"] ?>">
		</iframe>
		<div id="enemyCards"></div>
		<div id ="enemyHp">0</div>
		<div id = "enemyPicture"  onclick="attackHero()"></div>
		<div id="remainingTime">0</div>
		<div id="enemyRemainingCardsCount">0</div>
	</div>

	<div id="board">
		<div id='enemyBoardCards'></div>
		<div id="playerBoardCards"></div>
	</div>

	<div id="player">
		<div class = "ressourcesContainer">
			<div id="playerHp">0</div>
			<div id="playerGold">0</div>
			<div id="playerRemainingCardsCount">0</div>
		</div>
		<div id="playerCards"></div>
		<div class = "buttonsAction">
			<div id="endTurn" onclick="endTurn()">End Turn</div>
			<div id="heroPower" onclick="heroPower()">Hero Power</div>
		</div>

	</div>

<?php
	require_once("partial/footer.php");