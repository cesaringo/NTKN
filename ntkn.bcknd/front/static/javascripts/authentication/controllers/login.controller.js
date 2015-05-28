/**
* LoginController
* @namespace ntkn.authentication.controllers
*/
(function (){
	'use strict';

	angular
		.module('ntkn.authentication.controllers')
		.controller('LoginController', LoginController);

	LoginController.$inject = ['$location', '$scope', '$timeout', 'Authentication', 'Validate', 'ngProgress'];

	/**
	* @namespace LoginController
	*/
	function LoginController($location, $scope, $timeout, Authentication, Validate, ngProgress){
		

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
				ngProgress.start();
				ngProgress.color("#FAA634");
				ngProgress.height("5px");
				Authentication.login($scope.model.username, $scope.model.password)
				.then(function(response){
		        	// success case
		        	ngProgress.complete();
		        	$location.path("/dashboard");
		        },function(response){
		        	// error case
		            ngProgress.complete();
		        	$scope.errors = response;
		        });
			}
		}
	}
})();