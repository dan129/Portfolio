<?php
	require_once("action/CommonAction.php");

	class AjaxAction extends CommonAction {

		public function __construct() {
			parent::__construct(CommonAction::$VISIBILITY_MEMBER);
		}

		protected function executeAction() {
			$data = [];
			$data["key"] = $_SESSION["key"];
			$etat="";
			if (!empty($_POST["type"])) {
				if($_POST["type"] == "status"){
					$etat = parent::callAPI("games/state", $data);
				}
				else if($_POST["type"] == "playCard"){
					$data["type"] = "PLAY";
					$data["uid"] = $_POST["uid"];
					$etat = parent::callAPI("games/action", $data);
				}
				else if($_POST["type"] == "attack"){
					$data["type"] = "ATTACK";
					$data["uid"] = $_POST["uid"];
					$data["targetuid"] = $_POST["targetuid"];
					$etat = parent::callAPI("games/action", $data);
				}
				else if($_POST["type"] == "endTurn"){
					$data["type"] = "END_TURN";
					$etat = parent::callAPI("games/action", $data);
				}
				else if($_POST["type"] == "heroPower"){
					$data["type"] = "HERO_POWER";
					$etat = parent::callAPI("games/action", $data);
				}
			}

			if($etat === "INVALID_KEY"){
				header("location: login.php");
				exit;
			}

			return compact("etat");
		}
	}