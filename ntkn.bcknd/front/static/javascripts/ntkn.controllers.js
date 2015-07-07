(function(){
	'use strict';
	angular.module('ntkn')
 
	.controller('AppCtrl', function($scope, $state, AuthService, AUTH_EVENTS) {
		console.log("AppCtrl");

		//AUTH
		$scope.logout = function() {
			console.log()
    		AuthService.logout();
    		$state.go('login');
  		};

  		$scope.username = AuthService.username();
  		$scope.isAuthenticated = AuthService.isAuthenticated();


  		//Listen Events
		$scope.$on(AUTH_EVENTS.notAuthorized, function(event){
			console.log('You are not allowed to access this resource.');
    		$state.go('main.dash');
		});

		$scope.$on(AUTH_EVENTS.notAuthenticated, function(event){
			console.log('Sorry, You have to login again.');
			AuthService.logout();
			$state.go('login');
		});

		$scope.$on(AUTH_EVENTS.loginSuccess, function(){
			$scope.username = AuthService.username();
  			$scope.isAuthenticated = AuthService.isAuthenticated();
		});

		$scope.$on(AUTH_EVENTS.logoutSuccess, function(){
			$scope.username = undefined;
  			$scope.isAuthenticated = false;
		});

		$scope.setCurrentUsername = function(username) {
    		$scope.username = username;
  		};
	})

	/*Login Controller*/
	.controller('LoginCtrl', function($scope, $state, AuthService, Validate) {
		console.log('LoginCtrl');
		$scope.model = {'username':'','password':''};
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				AuthService.login($scope.model.username, $scope.model.password)
				.then(function(response){
		        	$state.go('main.dash', {}, {reload: true});
		        	$scope.setCurrentUsername($scope.model.username);
		        },function(response){
		        	$scope.errors = response;
		        });
			}
		}
	})

	.controller('DashCtrl', function($scope, $state, AuthService) {

	});





})()