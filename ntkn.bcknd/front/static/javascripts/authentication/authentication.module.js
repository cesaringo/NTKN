(function() {
	'use strict';

	angular
		.module('ntkn.authentication', [
			'ntkn.authentication.controllers',
			'ntkn.authentication.services',
			//'ntkn.authentication.interceptors',

		])

	angular
		.module('ntkn.authentication.controllers', []);

	angular
		.module('ntkn.authentication.services', ['ngCookies']);

	/*angular
		.module('ntkn.authentication.interceptors', []);*/
})();
