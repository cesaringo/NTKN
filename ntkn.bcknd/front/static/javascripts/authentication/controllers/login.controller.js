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
		$scope.model = {'username':'','password':''};
		$scope.complete = false;
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				Authentication.login($scope.model.username, $scope.model.password)
				.then(function(data){
		        	// success case
		        	console.log('$location.path("/")');
		        },function(data){
		        	// error case
		        	$scope.errors = data;
		        });
			}
		}
	}
})();