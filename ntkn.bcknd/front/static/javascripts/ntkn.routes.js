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
			.when('/login',{
				controller: 'LoginController',
				templateUrl: '/static/templates/authentication/login.html',
			})
			.when('/logout', {
		        templateUrl: '/static/templates/main.html',
		        controller: 'LogoutController',
		    })
		    .when('/dashboard', {
		        templateUrl: '/static/templates/dashboard.html',
		        controller: 'DashboardController',
		        
		        resolve: {
		          authenticated: ['Aunthentication', function(Aunthentication){
		            return Aunthentication.getAuthenticationStatus();
		          }],
		        }
		    })
			.otherwise('/');
	}
})()
