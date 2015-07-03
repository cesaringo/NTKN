(function(){
	'use strict';
	angular.module('ntkn')
	.service('AuthService', function($q, $http, $window){
		var isAuthenticated = false;
		var token = undefined;
		var username = undefined;

		function loadUserCredentials(){
			var _token = $window.localStorage.getItem('token');
			var _user =  JSON.parse($window.localStorage.getItem('user'));
			if (_token && _user.username){
				useCredentials(_token, _user.username);
			}
		}

		function storeUserCredentials(token, username){
			$window.localStorage.setItem('token', token);
			$window.localStorage.setItem('username', username);
			useCredentials(token, username);
		}

		function useCredentials(token, username){
			this.token = token;
			this.username = username;
			isAuthenticated = true;
			// Set the token as header for your requests!
			$http.defaults.headers.common.Authorization = 'Token ' + response.key;
		}

		function destroyUserCredentials() {
			delete $http.defaults.headers.common.Authorization;
			$window.localStorage.removeItem('token');
			$window.localStorage.removeItem('username');
			token = undefined;
			username = undefined;
			isAuthenticated = false;
		}

		var login = function (username, password){
			console.log("LoginService");
			return $http.post('/login', {username:username, password: password})
      			.then(function (response) {
        			console.log('Login Succesfully')
				});
		}

		var logout = function(){
			destroyUserCredentials();
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
  		}
	})

	
	.service('Validate', function(){
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

	})
 
	
})()