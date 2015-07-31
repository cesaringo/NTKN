(function(){
	'use strict';
	angular.module('ntkn', ['ui.router', 'http-auth-interceptor'])
	.config(function ($stateProvider, $urlRouterProvider) {
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
  			controller: 'DashCtrl'
  		})
  		.state('main.student',{
  			url: 'student',
  			templateUrl: '/static/views/student.html',
  			data: {
	      		authorizedRoles: ['student']
		    }
  		})
  		.state('main.admin', {
  			url: 'admin',
  			templateUrl: '/static/views/admin.html',
  			data: {
	      		authorizedRoles: ['admin']
		    }
  		})
  		.state('main.teacher', {
  			url: 'teacher',
  			templateUrl: '/static/views/teacher.html',
  			data: {
	      		authorizedRoles: ['teacher']
		    }
  		});
  		$urlRouterProvider.otherwise('/dash');
	})

	.run(function ($http){
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		//Authentication.initialize('//localhost:8000/rest-auth', false);
	})

})();
