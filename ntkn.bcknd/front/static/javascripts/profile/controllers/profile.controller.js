'use strict';

angular
	.module('ntkn.profile.controller')
	.controller('ProfileController', ProfileController);

ProfileController.$inject = ['$location', '$routeParams', 'ProfileService', 'Authentication'];

function ProfileController($location, $routeParams, ProfileService, Authentication) {
	if (!Authentication.authenticated) {
    	$location.path('/login');
    	return;
  	}

	var vm = this;
	vm.profile = undefined;
	activate();


	function activate(){
		ProfileService.get("me").then(profileSuccessFn, profileErrorFn);
			
		function profileSuccessFn(data, status, headers, config) {
			vm.profile = data;
      	}
		
		function profileErrorFn(data, status, headers, config) {
			console.log(data);
	    }
	}
}