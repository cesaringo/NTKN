(function(){
	'use strict';
	angular.module('ntkn')
 
	.controller('AppCtrl', function($scope, $rootScope, $state, AuthService, AUTH_EVENTS) {
		//console.log("AppCtrl");

		//AUTH
		$scope.logout = function() {
    			AuthService.logout();
    			$state.go('login');
  		};

  		$scope.username = AuthService.username();
  		$scope.isAuthenticated = AuthService.isAuthenticated();


  		//Listen Events
		$scope.$on(AUTH_EVENTS.notAuthorized, function(event){
			console.log('You are not allowed to access this resource.');
			$state.go('dashboard.profile', {}, {reload: true});
		});

		$scope.$on(AUTH_EVENTS.notAuthenticated, function(event){
			console.log('Sorry, You have to login again.');
			AuthService.logout();
			$state.go('login');
		});

		$scope.$on(AUTH_EVENTS.loginSuccess, function(){
			console.log('Login Succesfully');
			$scope.username = AuthService.username();
  			$scope.isAuthenticated = AuthService.isAuthenticated();
  			switch(AuthService.role()){
				case 'student': $state.go('dashboard.student', {}, {reload: true}); break;
				case 'teacher': $state.go('dashboard.teacher', {}, {reload: true}); break;
				case 'admin': 		$state.go('dashboard.admin', {}, {reload: true}); break;
				default: 
					$rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
					break;
			}
		});

		$scope.$on(AUTH_EVENTS.logoutSuccess, function(){
			$scope.username = undefined;
  			$scope.isAuthenticated = false;
		});

		$scope.setCurrentUsername = function(username) {
    		$scope.username = username;
  		};
	})

	/*Login Controller
	Login & Redirect to dashboard
	*/
	.controller('LoginCtrl', function($scope, $state, AuthService, Validate) {
		//console.log('LoginCtrl');
		$scope.model = {'username':'','password':''};
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				AuthService.login($scope.model.username, $scope.model.password)
				.then(function(response){
						$scope.setCurrentUsername($scope.model.username);
		        	},function(response){
		        		$scope.errors = response;
		        	});
			}
		}
	})

	.controller('ProfileCtrl', function($scope, SCEService) {
		console.log('ProfileCtrl');
		SCEService.UserProfile()
			.then(function(response){
				$scope.profile = response.data;
				//console.log($scope.profile);			
			}, function(response){
				console.log(response)
			});
	})

	.controller('DashCtrl', function($scope, $state, AuthService) {
		console.log("DashCtrl");
		console.log($state.current.data);
	});





})()