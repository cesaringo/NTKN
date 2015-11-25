'use strict';
angular
	.module('ntkn.authentication.controllers')
	.controller('DashboardController', DashboardController);

DashboardController.$inject = ['$scope', '$window', '$location', 'Authentication'];

function DashboardController($scope, $window, $location, Authentication){
	if (!Authentication.authenticated) {
    	$location.path('/login');
    	return;
  	}
  	$scope.token = $window.localStorage.token;
  	//$scope.user = JSON.parse($window.localStorage.user);
}