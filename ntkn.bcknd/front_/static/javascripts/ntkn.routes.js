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
				templateUrl: '/static/templates/main.html',
				controller: 'MainController',
			})
			.when('/register',{
				templateUrl: '/static/templates/authentication/register.html',
				controller: 'RegisterController',

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
		    })
			.otherwise('/');
	}
})()
