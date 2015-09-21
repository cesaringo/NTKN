(function(){
	'use strict';
	angular.module('ntkn')
	.constant('AUTH_EVENTS', {
		loginSuccess: 'auth-login-success',
		loginFailed: 'auth-login-failed',
		logoutSuccess: 'auth-logout-success',
		sessionTimeout: 'auth-session-timeout',
		notAuthenticated: 'auth-not-authenticated',
		notAuthorized: 'auth-not-authorized'
	})
	.constant('USER_ROLES', {
		admin: 'admin',
		student: 'student',
		teacher: 'teacher,'
	})
	.constant('SCE_API_URL', 'http://localhost:8000/sce-api')
	.constant('API_URL', 'http://localhost:8000/rest-auth');
})()