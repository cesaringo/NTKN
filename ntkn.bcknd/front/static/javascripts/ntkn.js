(function(){
	'use strict';
	angular.module('ntkn', ['ui.router'])
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
	  	.state('main.dash', { //All users can access, it can be profile data for example
    		url: 'main/dash',
 			templateUrl: '/static/views/dashboard.html',
  			controller: 'DashCtrl'
  		})
  		.state('main.admin', {
  			url: 'main/admin',
  			templateUrl: '/static/views/admin.html',
  			data: {
	      		authorizedRoles: ['admin']
		    }
  		})
  		.state('main.teacher', {
  			url: 'main/admin',
  			templateUrl: '/static/views/teaher.html',
  			data: {
	      		authorizedRoles: ['admin', 'teacher']
		    }
  		});
  		$urlRouterProvider.otherwise('/main/dash/');
	})

	.run(function ($http){
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		//Authentication.initialize('//localhost:8000/rest-auth', false);
	})

})();
