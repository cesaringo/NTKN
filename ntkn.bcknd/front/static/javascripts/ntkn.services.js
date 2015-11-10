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
		var user = undefined;

		function loadUserCredentials(){
			var _token = $window.localStorage.getItem('token');
			var _user =  JSON.parse($window.localStorage.getItem('user'));
			if (_token && _user){
				useCredentials(_token, _user);
			}
		}

		function storeUserCredentials(token, user){
			$window.localStorage.setItem('token', token);
			$window.localStorage.setItem('user', JSON.stringify(user));
			useCredentials(token, user);
		}

		function useCredentials(_token, _user){
			token = _token;
			user = _user;
			isAuthenticated = true;
			// Set the token as header for your requests!
			$http.defaults.headers.common.Authorization = 'Token ' + _token;
		}

        

		function destroyUserCredentials() {
			delete $http.defaults.headers.common.Authorization;
			$window.localStorage.removeItem('token');
			$window.localStorage.removeItem('user');
			token = undefined;
			user = undefined;
			isAuthenticated = false;
		}

		var login = function (username, password){
			console.log('LoginService');
			return $http.post(API_URL+'/auth/login/', {username:username, password: password})
	  			.then(function (response) {
	  				storeUserCredentials(response.data.key, response.data.user);
                    $rootScope.$broadcast(AUTH_EVENTS.loginSuccess, response.data);
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
    		return (isAuthenticated && authorizedRoles.indexOf(user.groups[0]) !== -1);
  		};

        //raises an error if token isn’t present
        var authenticationStatus = function(){
            var deferred = $q.defer();
            loadUserCredentials();
            if(token && user){
                deferred.resolve(user.username);
            }else{
                deferred.reject({error: "not-authenticated"});
            }
            return deferred.promise;
        }


  		loadUserCredentials();

  		return {
  			'login': login, 
  			'logout': logout,
  			'isAuthorized': isAuthorized,
  			'isAuthenticated': function() {return isAuthenticated;},
            'authenticationStatus': authenticationStatus,
  			'user': function() {return user;},
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
                return $http.get(API_URL + '/auth/user/');
            }
        };

        var StudentProfile = function(username){
            if (username != undefined){
                return $http.get(API_URL + '/alumni/students/'+username+'/');
            }
        };

        var GetCourses = function(params){
            return $http.get(API_URL + '/sce/courses/');
        };

        return {
            UserProfile: UserProfile,
            StudentProfile: StudentProfile,
            GetCourses: GetCourses,
        }
    }
	
})()