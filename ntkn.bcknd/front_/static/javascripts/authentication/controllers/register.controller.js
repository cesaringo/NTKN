(function () {
	'use strict';
	angular
		.module('ntkn.authentication.controllers')
		.controller('RegisterController', RegisterController);

	RegisterController.$inject = ['$location', '$scope', 'Authentication'];

	function RegisterController($location, $scope, Authentication){


		$scope.register = function(){
			var email = $scope.registerEmail;
			var username = $scope.registerUsername;
			var password = $scope.registerPassword;

			if (email && username && password) {
				Authentication.register(email, password, username);
			}
			else{
				$scope.registerError = 'Email, Username and password required';
			}
		}

		// If the user is authenticated, they should not be here.
		function activate() {
			if (Authentication.isAuthenticated()) {
				$location.url('/');
			}
		}
		
		
		
	}
})();