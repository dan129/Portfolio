<?php
	require_once("action/CommonAction.php");

	class QuitterAction extends CommonAction {

		public function __construct() {
			parent::__construct(CommonAction::$VISIBILITY_MEMBER);
		}

		protected function executeAction() {

			$key = array("key" => $_SESSION["key"]);
			$result = parent::callAPI("signout", $key);

			if($result == "SIGNED_OUT"){
				header("location: login.php");
			}


			return compact("result");
		}
	}