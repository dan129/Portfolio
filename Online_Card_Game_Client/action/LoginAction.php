<?php
	require_once("action/CommonAction.php");

	class LoginAction extends CommonAction {

		public function __construct() {
			parent::__construct(CommonAction::$VISIBILITY_PUBLIC);
		}

		protected function executeAction() {
			$result = null;

			$data = [];
			if (isset($_POST["username"]) && isset($_POST["password"])) {

				$data["username"] = $_POST["username"];
				$data["password"] = $_POST["password"];

				$result = parent::callAPI("signin", $data);

				if ($result == "INVALID_USERNAME_PASSWORD") {
					// err
				}
				else {
					$_SESSION["visibility"] = CommonAction::$VISIBILITY_MEMBER;
					$key = $result->key;
					$_SESSION["key"] = $key;
					header("location: accueil.php");
				}
			}

			return compact("result");
		}
	}
