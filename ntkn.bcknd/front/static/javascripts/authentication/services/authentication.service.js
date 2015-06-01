/**
* Authentication
* @namespace ntkn.authentication.services
*/
(function () {
	'use strict';

	angular
		.module('ntkn.authentication.services')
		.service('Authentication', Authentication);

	Authentication.$inject = ['$cookies', '$http', '$q', '$rootScope', '$window'];

	/**
	* @namespace Authentication
	* @returns (Factory)
	*/
	function Authentication($cookies, $http, $q, $rootScope, $window) {
		var Authentication = {
			'API_URL': '/rest-auth',
			'use_session': false,
	        'authenticated': null,
    	    'authPromise': null,

    	    //REQUEST SERVICE
			'request': function(args){
				// Let's retrieve the token if available
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
	            	var authentication = this;
	            	
		            if (status == 401){
		                delete $http.defaults.headers.common.Authorization;
		                $window.localStorage.removeItem('token');
		                //$window.localStorage.removeItem('username');
		                authentication.authenticated = false;
		                console.log(authentication.authenticated);
		                if (data.detail == "Invalid token.")
		                	$rootScope.$broadcast("Authentication.invalid_token");
		                else 
		                	$rootScope.$broadcast("Authentication.logged_out");
		            }
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
	                if (status == 403){
	                	var authentication = this;
	                	delete $http.defaults.headers.common.Authorization;
						$window.localStorage.removeItem('token');
						//$window.localStorage.removeItem('username');
						authentication.authenticated = false;
						$rootScope.$broadcast("Authentication.logged_out");
	                }
	                deferred.reject(data, status, headers, config);
	            }));
				return deferred.promise;
			},
			//END REQUEST SERVICE


			//REGISTER SERVICE
			'register': function (email, password, username){
		    	return $http.post('/auth/register', {
		    		username: username,
		    		password: password,
		    		email: email
		    	}).then(registerSuccessFn, registerErrorFn);
				function registerSuccessFn(data, status, headers, config){
					Authentication.login(email, password);
				}
				function registerErrorFn (argument) {
					console.error('Epic failure!');
				}
		    },
		    //END REGISTER SERVICE

		    //LOGIN SERVICE
			'login': function (username, password) {
				var auth = this;
				return this.request({
					'method': "POST",
					'url': "/login/",
					'data':{
	                    'username':username,
	                    'password':password
	                },
				}).then(loginSuccessFn);


				function loginSuccessFn(response){
					if(!auth.use_session){
						$http.defaults.headers.common.Authorization = 'Token ' + response.key;
						$window.localStorage.token = response.key; 
 						//$window.localStorage.username = response.data.username;
					}
					auth.authenticated = true;
					$rootScope.$broadcast("Authentication.logged_in", response);
				}
			},
			//END LOGIN SERVICE

			//LOGOUT SERVICE
			'logout': function (){
				var authentication = this;
				return this.request({
	                'method': "POST",
	                'url': "/logout/"
	            }).then(logoutSuccessFn, logoutErrorFn);

				function logoutSuccessFn (response) {
					delete $http.defaults.headers.common.Authorization;
					$window.localStorage.removeItem('token');
					//$window.localStorage.removeItem('username');
					authentication.authenticated = false;
					$rootScope.$broadcast("Authentication.logged_out");
				}
				function logoutErrorFn (argument) {
					console.error(argument);
				}
			},
			//END LOGOUT SERVICE


			'changePassword': null,
			'resetPassword': null,
			'profile': null, 
			'updateProfile': null, 
			'verify': null,
			'confirmReset': null, 
			
			
			

			'authenticationStatus': function(restrict, force){
	            // Set restrict to true to reject the promise if not logged in
	            // Set to false or omit to resolve when status is known
	            // Set force to true to ignore stored value and query API
	            console.log("Cheking authenticationStatus");

	            restrict = restrict || false;
	            force = force || false;
	            if(this.authPromise == null || force){
	                this.authPromise = this.request({
	                    'method': "GET",
	                    'url': "/user/"
	                })
	            }
	            var da = this;
	            var getAuthStatus = $q.defer();
	            if(this.authenticated != null && !force){
	                // We have a stored value which means we can pass it back right away.
	                if(this.authenticated == false && restrict){
	                    getAuthStatus.reject("User is not logged in.");
	                }else{
	                    getAuthStatus.resolve();
	                }
	            }else{
	                // There isn't a stored value, or we're forcing a request back to
	                // the API to get the authentication status.
	                this.authPromise.then(function(){
	                	//console.log('this.authPromise.then success');
	                    da.authenticated = true;
	                    getAuthStatus.resolve();
	                },function(){
	                    da.authenticated = false;
	                    if(restrict){
	                        getAuthStatus.reject("User is not logged in.");
	                    }else{
	                        getAuthStatus.resolve();
	                    }
	                });
	            }
	            return getAuthStatus.promise;
	        },
	        'initialize': function (url, sessions){
				this.API_URL = url;
	            this.use_session = sessions;
	            return this.authenticationStatus();
			},

			'getAuthenticationStatus': function(){
				return this.request({
	                'method': "GET",
	                'url': "/user/"
	            }).then(getAuthenticationStatusSuccessFn, logoutErrorFn);

	            function getAuthenticationStatusSuccessFn(){
	            	console.log("getAuthenticationStatusSuccessFn");
	            }
	            function getAuthenticationStatusErrorFn(){
	            	console.log("getAuthenticationStatusErrorFn");
	            }
	            
			},
		};
		return Authentication;
	}
})();	