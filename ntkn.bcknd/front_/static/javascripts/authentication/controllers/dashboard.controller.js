'use strict';
angular
	.module('ntkn.authentication.controllers')
	.controller('DashboardController', DashboardController);

DashboardController.$inject = ['$scope', '$window', '$location', 'Authentication'];

function DashboardController($scope, $window, $location, Authentication){
	if (!$window.localStorage.token) {
    	$location.path('/login');
    	return;
  	}
  	$scope.token = $window.localStorage.token;
  	$scope.authenticated = Authentication.authenticated;
  	//$scope.username = $window.localStorage.username;
}