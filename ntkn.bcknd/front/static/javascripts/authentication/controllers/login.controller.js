/**
* LoginController
* @namespace ntkn.authentication.controllers
*/
(function (){
	'use strict';

	angular
		.module('ntkn.authentication.controllers')
		.controller('LoginController', LoginController);

	LoginController.$inject = ['$location', '$scope', 'Authentication', 'Validate'];

	/**
	* @namespace LoginController
	*/
	function LoginController($location, $scope, Authentication, Validate){
		if (Authentication.authenticated) {
	    	$location.path('/dashboard');
	    	return;
	  	}
		$scope.model = {'username':'','password':''};
		$scope.complete = false;
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				console.log("No errror");
				Authentication.login($scope.model.username, $scope.model.password)
				.then(function(response){
		        	// success case
		        	$location.path("/dashboard");
		        },function(response){
		        	// error case
		        	$scope.errors = data;
		        });
			}
		}
	}
})();