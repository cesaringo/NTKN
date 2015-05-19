(function(){
	'use strict';

	angular
		.module('ntkn.config')
		.config(config);

	config.$inject = ['$httpProvider', '$locationProvider'];

	/**
  	* @name config
  	* @desc Enable HTML5 routing
  	*/
  	function config($httpProvider, $locationProvider) {
  		$locationProvider.html5Mode(true);
  		$locationProvider.hashPrefix('!');
      //$httpProvider.interceptors.push('AuthInterceptor');
  	}
})();