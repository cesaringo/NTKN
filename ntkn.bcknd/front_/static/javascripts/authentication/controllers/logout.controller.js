(function (){
	'use strict';
	angular
		.module('ntkn.authentication.controllers')
		.controller('LogoutController', function ($scope, $location, Authentication) {
			Authentication.logout()
			.then(function(data){
	        	$location.path("/");
	        },function(data){
	        	// error case
	        	$scope.errors = data;
	        });
		});

})();