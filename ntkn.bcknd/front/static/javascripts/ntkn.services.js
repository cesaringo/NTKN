(function(){
	'use strict';
	angular.module('ntkn')
	.service('AuthService', AuthService)
    .service('SCEService', SCEService)
	.service('Validate', Validate);


	AuthService.$inject = ['$q', '$http', '$window', '$rootScope', 'API_URL', 'AUTH_EVENTS'];
	function AuthService($q, $http, $window, $rootScope, API_URL, AUTH_EVENTS){
		var isAuthenticated = false;
		var token = undefined;
		var username = undefined;
        var role = undefined;

		function loadUserCredentials(){
			console.log('loadUserCredentials')
			var _token = $window.localStorage.getItem('token');
			var _username =  $window.localStorage.getItem('username');
            var _role =  $window.localStorage.getItem('role');
			if (_token && _username){
				useCredentials(_token, _username, _role);
			}
		}

		function storeUserCredentials(token, username, role){
			$window.localStorage.setItem('token', token);
			$window.localStorage.setItem('username', username);
            $window.localStorage.setItem('role', role);
			useCredentials(token, username, role);
		}

		function useCredentials(_token, _username, _role){
			token = _token;
			username = _username;
            role = _role;
			isAuthenticated = true;
			// Set the token as header for your requests!
			$http.defaults.headers.common.Authorization = 'Token ' + _token;
		}

		function destroyUserCredentials() {
			delete $http.defaults.headers.common.Authorization;
			$window.localStorage.removeItem('token');
			$window.localStorage.removeItem('username');
            $window.localStorage.removeItem('role');
			token = undefined;
			username = undefined;
			isAuthenticated = false;
		}

		var login = function (username, password){
			console.log('LoginService');
			return $http.post(API_URL+'/login/', {username:username, password: password})
	  			.then(function (response) {
                    var role = getCurrentRole(response.data.user.groups);
	  				storeUserCredentials(response.data.key, 
                        response.data.user.username, role) 
                    $rootScope.$broadcast(AUTH_EVENTS.loginSuccess, response.data);
	    			console.log('Login Succesfully');
                    console.log(response);
				});
		}

        var getCurrentRole = function(roles){
            if (roles == undefined) // Si no tiene ningun role
                return undefined //Permision denegado. todos los usuarios deben de tener un rol
            var role = "";
            if (roles.length > 1){//Muchos roles. Preguntar al usuario que Role quiere usar
                ///var role ...
            }else{
                role = roles[0];
            }
            return role;
        }

		var logout = function(){
			destroyUserCredentials();
            $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
		}

		var isAuthorized = function(authorizedRoles) {
    		if (!angular.isArray(authorizedRoles)) {
      			authorizedRoles = [authorizedRoles];
    		}
    		return (isAuthenticated && authorizedRoles.indexOf(role) !== -1);
  		};

  		loadUserCredentials();

  		return {
  			'login': login, 
  			'logout': logout,
  			'isAuthorized': isAuthorized,
  			'isAuthenticated': function() {return isAuthenticated;},
  			'username': function() {return username;},
            'role': function() {return role;},
  		}
	}

	function Validate(){
		return {
            'message': {
                'minlength': 'This value is not long enough.',
                'maxlength': 'This value is too long.',
                'email': 'A properly formatted email address is required.',
                'required': 'This field is required.'
            },
            'more_messages': {
                'demo': {
                    'required': 'Here is a sample alternative required message.'
                }
            },
            'check_more_messages': function(name,error){
                return (this.more_messages[name] || [])[error] || null;
            },
            validation_messages: function(field,form,error_bin){
                var messages = [];
                for(var e in form[field].$error){
                    if(form[field].$error[e]){
                        var special_message = this.check_more_messages(field,e);
                        if(special_message){
                            messages.push(special_message);
                        }else if(this.message[e]){
                            messages.push(this.message[e]);
                        }else{
                            messages.push("Error: " + e)
                        }
                    }
                }
                var deduped_messages = [];
                angular.forEach(messages, function(el, i){
                    if(deduped_messages.indexOf(el) === -1) deduped_messages.push(el);
                });
                if(error_bin){
                    error_bin[field] = deduped_messages;
                }
            },
            'form_validation': function(form,error_bin){
                for(var field in form){
                    if(field.substr(0,1) != "$"){
                        this.validation_messages(field,form,error_bin);
                    }
                }
            }
        }

	}

    SCEService.$inject = ['$q', '$http', 'API_URL'];
    function SCEService ($q, $http, API_URL){

        var UserProfile = function(username){
            if (username == undefined || username == "" || username == null){
                return $http.get(API_URL + '/user/');
            }
        }

        return {
            UserProfile: UserProfile,
        }
    }
	
})()