<?php
	require_once("action/LoginAction.php");

	$action = new LoginAction();
	$data = $action->execute();

	require_once("partial/header.php");
?>

		<div class="login-form-frame">
			<form action="login.php" method="post">
				<?php
					if ($data["result"] == "INVALID_USERNAME_PASSWORD") {
						?>
						<div class="error-div"><strong>Erreur : </strong>Connexion erronée</div>
						<?php
					}
				?>
				<div class="form-input">
					<input type="text" name="username" placeholder="Nom d'usager"/>
				</div>
				<div class="form-separator"></div>
				<div class="form-input">
					<input type="password" name="password" placeholder="Mot de passe"/>
				</div>
				<div class="form-separator"></div>
				<div class="form-input">
					<input id="connexion" type="image" src="images/do.png">
				</div>
				<div class="form-separator"></div>
			</form>
		</div>
		<canvas id="canvas" ></canvas>
<?php
	require_once("partial/footer.php");
