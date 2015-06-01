/**
* LoginController
* @namespace ntkn.authentication.controllers
*/
(function (){
	'use strict';
	angular
		.module('ntkn.authentication.controllers')
		.controller('LoginController', LoginController);
	LoginController.$inject = ['$location', '$timeout', '$scope', '$interval', 'Authentication', 'Validate', 'ngProgress'];
	function LoginController($location, $timeout, $scope, $interval, Authentication, Validate, ngProgress){
		

		if (Authentication.authenticated) {
			console.log(Authentication.authenticated);
	    	$location.path('/dashboard');
	    	return;
	  	}
		$scope.model = {'username':'','password':''};
		$scope.complete = false;
		$scope.login = function(formData){
			//
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				
				var _startProgressBar;
				startProgressBar();

				$timeout(function(){//Nice Animation
					Authentication.login($scope.model.username, $scope.model.password)
					.then(function(response){
			        	//success case
			        	completeProgressBar();
			        	$location.path("/dashboard");
			        },function(response){
			        	completeProgressBar();
			        	$scope.errors = response;
			        });
				},100);
			}

			function startProgressBar(){
				$scope.loginProgress = true;
				var progressCount = 0;
				_startProgressBar = $interval(function(){
					var remaining = 100 - progressCount;
					progressCount +=  (0.15 * Math.pow(1 - Math.sqrt(remaining), 2));
					$scope.progressCount = progressCount;
					//console.log("startProgressBar" + $scope.progressCount);
				}, 100);
			}
			function completeProgressBar(){
				$interval.cancel(_startProgressBar);
				$scope.loginProgress = false;
				var progressCount = 0;
				$scope.progressCount = progressCount;
			}
		}
	}
})();