(function (){
	'use strict';

	angular
		.module('ntkn.routes')
		.config(config);

	config.$inject = ['$routeProvider'];

	/**
	* @name config
	* @desc Define valid aplication routes
	*/
	function config($routeProvider){
		$routeProvider
			.when('/', {
				templateUrl: '/static/templates/main.html', //or main.html
				controller: 'MainController',
				resolve: {
		          authenticated: ['Authentication', function(Authentication){
		            return Authentication.authenticationStatus();
		          }],
		        }
			})
			.when('/login',{
				controller: 'LoginController',
				controllerAs: 'vm',
				templateUrl: '/static/templates/authentication/login.html',
			})
			.when('/logout', {
		        templateUrl: '/static/templates/main.html',
		        controller: 'LogoutController',
		        resolve: {
		          authenticated: ['Authentication', function(Authentication){
		            return Authentication.authenticationStatus();
		          }],
		        }
		    })
		    .when('/dashboard', {
		        templateUrl: '/static/templates/dashboard.html',
		        controller: 'DashboardController',
		        resolve: {
		          authenticated: ['Authentication', function(Authentication){
		            return Authentication.authenticationStatus();
		          }],
		        }
		    })
			.otherwise('/');
	}
})()
