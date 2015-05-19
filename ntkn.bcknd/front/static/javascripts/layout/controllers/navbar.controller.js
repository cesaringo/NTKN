/**
* NavbarController
* @namespace ntkn.layout.controllers
*/
(function (){
	'use strict';

	angular
		.module('ntkn.layout.controllers')
		.controller('NavbarController', NavbarController);

	NavbarController.$inject = ['$scope', 'Authentication'];

	/**
	* @namespace NavbarController
	*/
	function NavbarController ($scope, Authentication) {
		var vm = this;
		vm.logout = logout;

		/**
	    * @name logout
	    * @desc Log the user out
	    * @memberOf ntkn.layout.controllers.NavbarController
	    */
	    function logout (argument) {
	    	Authentication.logout();
	    }
	}

})();