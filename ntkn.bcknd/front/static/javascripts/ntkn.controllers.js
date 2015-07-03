(function(){
	'use strict';
	angular.module('ntkn')
 
	.controller('AppCtrl', function($scope, $state, AuthService, AUTH_EVENTS) {
		console.log("AppCtrl");
		$scope.username = AuthService.username();
		$scope.$on(AUTH_EVENTS.notAuthorized, function(event){
			console.log('You are not allowed to access this resource.');
    		$state.go('main.dash');
		});
		$scope.$on(AUTH_EVENTS.notAuthenticated, function(event){
			console.log('Sorry, You have to login again.');
			AuthService.logout();
			$state.go('login');
		});
		$scope.setCurrentUsername = function(username) {
    		$scope.username = username;
  		};
	})
	.controller('LoginCtrl', function($scope, $state, AuthService, Validate) {
		console.log('LoginCtrl');
		$scope.model = {'username':'','password':''};
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				AuthService.login()
				.then(function(response){
		        	$state.go('main.dash', {}, {reload: true});
		        	$scope.setCurrentUsername($scope.model.username);
		        },function(response){
		        	$scope.errors = response;
		        });
			}
		}
	})
	.controller('DashCtrl', function() {

	});
})()