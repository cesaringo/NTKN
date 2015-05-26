/**
* Authentication
* @namespace ntkn.authentication.services
*/
(function () {
	'use strict';

	angular
		.module('ntkn.authentication.services')
		.service('Authentication', Authentication);

	Authentication.$inject = ['$cookies', '$http', '$q', '$rootScope'];

	/**
	* @namespace Authentication
	* @returns (Factory)
	*/
	function Authentication($cookies, $http, $q, $rootScope) {
		var Authentication = {
			'API_URL': '/rest-auth',
			'use_session': true,
	        'authenticated': null,
    	    'authPromise': null,
			'request': request,
			'register': register,
			'login': login,
			'logout': logout,
			'changePassword': null,
			'resetPassword': null,
			'profile': null, 
			'updateProfile': null, 
			'verify': null,
			'confirmReset': null, 
			
			'getAuthenticatedAccount': getAuthenticatedAccount,
			'isAuthenticated': isAuthenticated,
			'setAuthenticatedAccount': setAuthenticatedAccount,
			'unauthenticate': unauthenticate,
			

			'authenticationStatus': function(restrict, force){
	            // Set restrict to true to reject the promise if not logged in
	            // Set to false or omit to resolve when status is known
	            // Set force to true to ignore stored value and query API

	            
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
	        'initialize': initialize,
		};
		return Authentication;

		function request(args){
			// Let's retrieve the token from the cookie, if available
            if($cookies.token){
                $http.defaults.headers.common.Authorization = 'Token ' + $cookies.token;
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
            	deferred.resolve(data, status);
            }))
            .error(angular.bind(this,function(data, status, headers, config){
            	console.log("error syncing with: " + url);
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

		/**
	    * @name register
	    * @desc Try to register a new user
	    * @param {string} username The username entered by the user
	    * @param {string} password The password entered by the user
	    * @param {string} email The email entered by the user
	    * @returns {Promise}
	    * @memberOf ntkn.authentication.services.Authentication
	    */
	    function register(email, password, username){
	    	return $http.post('/auth/register', {
	    		username: username,
	    		password: password,
	    		email: email
	    	}).then(registerSuccessFn, registerErrorFn);

	    	/**
			* @name registerSuccessFn
			* @desc Log the new user in
			*/
			function registerSuccessFn(data, status, headers, config){
				Authentication.login(email, password);
			}

			/**
			* @name registerErrorFn
			* @desc Log "Epic failure!" to the console
			*/
			function registerErrorFn (argument) {
				console.error('Epic failure!');
			}
	    }

		/**
		* @name login
		* @desc Try to log in with email `email` and password `password`
		* @param {string} email The email entered by the user
		* @param {string} password The password entered by the user
		* @returns {Promise}
		* @memberOf ntkn.authentication.services.Authentication
		*/
		function login(username, password) {
			var auth = this;
			return this.request({
				'method': "POST",
				'url': "/login/",
				'data':{
                    'username':username,
                    'password':password
                },
			}).then(loginSuccessFn);


			function loginSuccessFn(data){
				console.log(data)
				if(!auth.use_session){
					$http.defaults.headers.common.Authorization = 'Token ' + data.key;
					$cookies.token = data.key;
					console.log('$http=');
				}
				auth.authenticated = true;
				$rootScope.$broadcast("Authentication.logged_in", data);
			}
			
		}

		/**
		* @name getAuthenticatedAccount
		* @desc Return the currently authenticated account
		* @returns {object|undefined} Account if authenticated, else `undefined`
		* @memberOf thinkster.authentication.services.Authentication
		*/
		function getAuthenticatedAccount(){
			if (!$cookies.authenticatedAccount){
				return ;
			}

			return JSON.parse($cookies.authenticatedAccount);
		}
		

		/**
		* @name isAuthenticated
		* @desc Check if the current user is authenticated
		* @returns {boolean} True is user is authenticated, else false.
		* @memberOf ntkn.authentication.services.Authentication
		*/
		function isAuthenticated() {
			return !!$cookies.authenticatedAccount;
		}

		/**
		* @name setAuthenticatedAccount
		* @desc Stringify the account object and store it in a cookie
		* @param {Object} user The account object to be stored
		* @returns {undefined}
		* @memberOf ntkn.authentication.services.Authentication
		*/
		function setAuthenticatedAccount(account) {
			$cookies.authenticatedAccount = JSON.stringify(account);
		}

		/**
		* @name unauthenticate
		* @desc Delete the cookie where the user object is stored
		* @returns {undefined}
		* @memberOf ntkn.authentication.services.Authentication
		*/
		function unauthenticate() {
			delete $cookies.authenticatedAccount;
		}


		/**
		* @name logout
		* @desc Try to log the user out
		* @returns {Promise}
		* @memberOf ntkn.authentication.services.Authentication
		*/
		function logout(){
			var authentication = this;
			return this.request({
                'method': "POST",
                'url': "/logout/"
            }).then(logoutSuccessFn, logoutErrorFn);

			function logoutSuccessFn (response) {
				delete $http.defaults.headers.common.Authorization;
				delete $cookies.token;
				authentication.authenticated = false;
				$rootScope.$broadcast("Authentication.logged_out");
			}
			function logoutErrorFn (argument) {
				console.error(argument);
			}
		}

		function initialize(url, sessions){
			this.API_URL = url;
            this.use_session = sessions;
            return this.authenticationStatus();
		}


	}
})();	