(function (){
	'use strict';

	angular
		.module('ntkn.authentication.interceptors')
		.service('AuthInterceptor', AuthInterceptor);


	AuthInterceptor.$inject = ['$injector', '$location'];

	function AuthInterceptor($injector, $location){
		var AuthInterceptor = {
			request: function (config) {
				var Auth = $injector.get('Authentication');
				try{
					var token = Auth.getAuthenticatedAccount().auth_token;
					if (token) {
					  //config.headers['Authorization'] = 'Token ' + token;
					}
				}catch(e){
					//console.log(e)
				}
				return config;
			},
			//requestError: function(){},

			//response: function(){},

			responseError: function (response) {
				if (response.status === 403) {
				    $location.path('/login');
				}
				return response;
			},
		}

		return AuthInterceptor;
	}
})();