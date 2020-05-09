<?php
	require_once("action/CommonAction.php");

	class AccueilAction extends CommonAction {

		public function __construct() {
			parent::__construct(CommonAction::$VISIBILITY_PUBLIC);
		}

		protected function executeAction() {
			$result="";
			if($_SESSION["visibility"]!= CommonAction::$VISIBILITY_MEMBER){
				header("location: login.php");
				exit;
			}
			else{
				$data["key"]= $_SESSION["key"];
				if(!empty($_GET["logout"])){
					$result = parent::callAPI("signout", $data);

					if($result == "SIGNED_OUT"){
						session_unset();
						session_destroy();
						session_start();
						header("location: login.php");
						exit;
					}else{
						var_dump($result);exit;
					}
				}
				if(!empty($_GET["pvp"])){
					$data["type"] = "PVP";
					$result = parent::callAPI("games/auto-match", $data);
					if($result == "JOINED_PVP" || $result == "CREATED_PVP" && $result != "INVALID_KEY" ){
						header("location: game.php");
						exit;
					}else{var_dump($result);}
				}
				if(!empty($_GET["training"])){
					$data["type"] = "TRAINING";
					$result = parent::callAPI("games/auto-match", $data);
					if($result == "JOINED_TRAINING" && $result != "INVALID_KEY" ){
						header("location: game.php");
						exit;
					}else{
						var_dump($result);exit;
					}
				}
				if($result == "INVALID_KEY"){
					header("location: login.php");exit;
				}
			}
		}
	}