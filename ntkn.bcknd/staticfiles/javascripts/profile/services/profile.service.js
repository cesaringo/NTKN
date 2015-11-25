'use strict';
angular
	.module('ntkn.profile.service')
	.service('ProfileService', ProfileService);

ProfileService.$inject = ['$http', '$window', '$q', '$cookies', '$rootScope', 'Authentication'];

function ProfileService($http, $window, $q, $cookies, $rootScope, Authentication){
	var Profile = {
		'API_URL': '/rest-auth',
      	'get': get,
      	//'update': update,
    };

   	return Profile;

   	

   	function get(username) {
		return Authentication.request({
			'method': "GET",
			'url': "/user/",
		});
    }
}