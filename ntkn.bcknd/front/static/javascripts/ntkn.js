(function(){
	'use strict';
	angular.module('ntkn', ['ui.router', 'http-auth-interceptor'])
	.config(function ($stateProvider, $urlRouterProvider, USER_ROLES) {
		$stateProvider
		.state('login', {
			url: '/login',
			templateUrl: '/static/views/authentication/login.html',
			controller: 'LoginCtrl'
		})
		.state('main', {
		    url: '/',
		    abstract: true,
		    templateUrl: '/static/views/main.html'
	  	})
	  	.state('main.profile', {
    		url: 'profile',
 			templateUrl: '/static/views/profile.html',
  			controller: 'ProfileCtrl'
  		})
	  	.state('main.dash', { //All users can access, it can be profile data for example
    		url: 'dash',
 			templateUrl: '/static/views/dashboard.html',
  			controller: 'DashCtrl',
  			data: {
	      		authorizedRoles: [USER_ROLES.admin, USER_ROLES.teacher, USER_ROLES.student]
		    }
  		})
  		.state('main.student',{
  			url: 'student',
  			templateUrl: '/static/views/student.html',
  			data: {
	      		authorizedRoles: [USER_ROLES.student]
		    }
  		})
  		.state('main.admin', {
  			url: 'admin',
  			templateUrl: '/static/views/admin.html',
  			data: {
	      		authorizedRoles: [USER_ROLES.admin]
		    }
  		})
  		.state('main.teacher', {
  			url: 'teacher',
  			templateUrl: '/static/views/teacher.html',
  			data: {
	      		authorizedRoles: [USER_ROLES.teacher]
		    }
  		});
  		$urlRouterProvider.otherwise('/dash');
	})

	.run(function ($http, $rootScope, $state, AuthService, AUTH_EVENTS){
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		$rootScope.$on('$stateChangeStart', function(event,next, nextParams, fromState){
			console.log("stateChangeStart");
			if('data' in next && 'authorizedRoles' in next.data){
				console.log(next);
				console.log($state.current);
				var authorizedRoles = next.data.authorizedRoles;
				if (!AuthService.isAuthorized(authorizedRoles)){
					event.preventDefault();
					$state.go($state.current, {}, {reload: true});
					$rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
				}
			}
		});

		//Authentication.initialize('//localhost:8000/rest-auth', false);
	})

})();
