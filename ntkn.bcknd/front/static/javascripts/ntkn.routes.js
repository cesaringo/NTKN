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
				templateUrl: '/static/views/main.html',
				controller: 'MainController',
			})
			.when('/login',{
				controller: 'LoginController',
				templateUrl: '/static/views/authentication/login.html',
			})
			.when('/logout', {
		        templateUrl: '/static/views/main.html',
		        controller: 'LogoutController',
		    })
		    .when('/dashboard', {
		        templateUrl: '/static/views/dashboard.html',
		        controller: 'DashboardController',
		    })
			.otherwise('/');
	}
})()
