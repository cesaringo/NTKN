'use strict';

angular
	.module('ntkn.profile.controller')
	.controller('ProfileController', ProfileController);

ProfileController.$inject = ['$location', '$routeParams', 'ProfileService'];

function ProfileController($location, $routeParams, ProfileService) {
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