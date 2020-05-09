<?php
	require_once("action/AccueilAction.php");

	$action = new AccueilAction();
	$action->execute();

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<link rel="stylesheet" href="css/accueil.css">
	<script src="js/accueilAnimation.js"></script>
	<title>Document</title>
</head>
<body>
	<div class='boutons'>
		<div><a href="?training=true">Pratiquer</a></div>
		<div><a href="?pvp=true">Jouer</a></div>
		<div><a href="?logout=true">Quitter</a></div>
	</div>
	<img id="canvas" >

	<iframe
		src="https://magix.apps-de-cours.com/server/#/chat/<?= $_SESSION["key"] ?>">
	</iframe>

<?php
	require_once("partial/footer.php");