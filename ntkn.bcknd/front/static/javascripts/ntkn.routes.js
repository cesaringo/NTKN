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
	function config($routeProvider ){
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
		        controller: 'LogoutController',
		        templateUrl: '/static/views/main.html',
		    })
		    .when('/dashboard', {
		        templateUrl: '/static/views/dashboard.html',
		        controller: 'DashboardController',
		        resolve: {
		        	authenticated: ['Authentication', function(Authentication){
		        		console.log("dashboard");
			            return Authentication.authenticationStatus();
			        }],
		        },
		        

		    })
		    .when('/profile',{
		    	templateUrl: '/static/views/profile.html',
		    	controller: 'ProfileController',
		    	controllerAs: 'vm',
		    	resolve: {
					authenticated: ['Authentication', function(Authentication){
						console.log("profile");
			            return Authentication.authenticationStatus();
			        }],
		    	},
		    	
		    })
			.otherwise('/');
	}
})()
