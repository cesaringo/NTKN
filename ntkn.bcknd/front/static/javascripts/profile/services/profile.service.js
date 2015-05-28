'use strict';
angular
	.module('ntkn.profile.service')
	.service('ProfileService', ProfileService);

ProfileService.$inject = ['$http', '$window', '$q', '$cookies'];

function ProfileService($http, $window, $q, $cookies){
	var Profile = {
		'API_URL': '/rest-auth',
		'request': request,
      	'get': get,
      	//'update': update,
    };

   	return Profile;

   	function request (args){
   		// Let's retrieve the token from the cookie, if available
        if($window.localStorage.token){
            $http.defaults.headers.common.Authorization = 'Token ' + $window.localStorage.token;
        }
        //Continue
        params = args.params || {}
        args = args || {};
        var deferred = $q.defer(),
        	url = this.API_URL + args.url,
        	method = args.method || "GET",
        	params = params,
        	data = args.data || {};
        
        // Fire the request, as configured.
        $http({
            url: url,
            withCredentials: this.use_session,
            method: method.toUpperCase(),
            headers: {'X-CSRFToken': $cookies['csrftoken']},
            params: params,
            data: data
        })
        .success(angular.bind(this, function(data, status, headers, config){
        	//console.log(config);
        	deferred.resolve(data, status);
        }))
        .error(angular.bind(this,function(data, status, headers, config){
        	console.log("error syncing with: " + url);
        	//console.log(config);
        	//Set request status
        	if(data){
        		data.status = status;
        	}
        	if(status == 0){
                if(data == ""){
                    data = {};
                    data['status'] = 0;
                    data['non_field_errors'] = ["Could not connect. Please try again."];
                }
                // or if the data is null, then there was a timeout.
                if(data == null){
                    // Inject a non field error alerting the user
                    // that there's been a timeout error.
                    data = {};
                    data['status'] = 0;
                    data['non_field_errors'] = ["Server timed out. Please try again."];
                }
            }
            deferred.reject(data, status, headers, config);
        }));
		return deferred.promise;
   	}

   	function get(username) {
		return this.request({
			'method': "GET",
			'url': "/user/",
		});
    }
}