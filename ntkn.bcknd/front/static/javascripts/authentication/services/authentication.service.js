/**
* Authentication
* @namespace ntkn.frnt.authentication.services
*/
(function () {
	'use strict';

	angular
		.module('ntkn.front.authentication.services')
		.factory('Authentication', Authentication);

	Authentication.$inject = ['$cookies', '$http'];

	/**
	* @namespace Authentication
	* @returns (Factory)
	*/
	function Authentication($cookies, $http) {
		var Authentication = {
			register: register
		};
		return Authentication;
	}

	/**
    * @name register
    * @desc Try to register a new user
    * @param {string} username The username entered by the user
    * @param {string} password The password entered by the user
    * @param {string} email The email entered by the user
    * @returns {Promise}
    * @memberOf ntkn.frnt.authentication.services.Authentication
    */
    function register(email, password, username){
    	return $http.post('/auth/register/', {
    		username: username,
    		password: password,
    		email: email
    	})
    }


})();