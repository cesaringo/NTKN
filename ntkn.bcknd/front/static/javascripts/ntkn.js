(function(){
	'use strict';

	angular
		.module('ntkn', [
			'ntkn.config',
			'ntkn.routes',
			'ntkn.authentication',
			'ngProgress',
		]);

	angular
		.module('ntkn.routes', ['ngRoute']);

	angular
		.module('ntkn.config', []);
	
	angular
		.module('ntkn')
		.run(run);

	run.$inject = ['$http', 'Authentication'];

	/**
	* @name run
	* @desc Update xsrf $http headers to align with Django's defaults 
	**/

	function run($http, Authentication){
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		//Authentication.initialize('//localhost:8000/rest-auth', false);
	}

})();
