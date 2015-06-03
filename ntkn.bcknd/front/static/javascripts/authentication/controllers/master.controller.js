(function(){
	'use strict';
	angular
		.module('ntkn.authentication.controllers')
		.controller('MasterController', MasterController);

	MasterController.$inject = ['$scope', '$location', '$window', 'Authentication', ];

	function MasterController($scope, $location, $window, Authentication){
		// Assume user is not logged in until we hear otherwise
		$scope.authenticated = false;
		$scope.username = "..";
		
		// Wait for the status of authentication, set scope var to true if it resolves
		Authentication.authenticationStatus(true).then(function(){
	        $scope.authenticated = true;
	    });

	    
	    // Wait and respond to the logout event.
	    $scope.$on('Authentication.logged_out', function() {
      		$scope.authenticated = false;
      		$scope.username = null;
		});

		// Wait and respond to the log in event.
		$scope.$on('Authentication.logged_in', function() {
	      $scope.authenticated = true;
	      $scope.username = $window.localStorage.username;
	    });

	    $scope.$on('Authentication.invalid_token', function() {
			$scope.authenticated = false;
			$scope.username = null;
			$scope.invalid_token = "Token has expired or is invalid. Please login again";
			$location.path("/login");
	    });


	    //If the user attempts to access a restricted page, redirect them back to the main page.
	    $scope.$on('$routeChangeError', function(ev, current, previous, rejection){
	      console.error("Unable to change routes.  Error: ", rejection)
	      $location.path('/restricted').replace();
	    });


	    
	}
})();