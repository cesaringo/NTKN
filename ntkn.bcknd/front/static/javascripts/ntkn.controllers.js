(function(){
	'use strict';
	angular.module('ntkn')
 
	.controller('AppCtrl', function($scope, $rootScope, $state, AuthService, $mdSidenav, $mdComponentRegistry, $log,$mdUtil,  AUTH_EVENTS) {

		var self = this;

		//Main sidenav//
		$scope.lockMainSideNav = true; //Alway show ond desktop
		$scope.toggleMainSideNav = buildToggler('mainSideNav');
		$scope.close = function () {
		 $mdSidenav('mainSideNav').close()
		   .then(function () {
		     $log.debug("close mainSideNav is done");
		   });
		};
		/**
	     * Build handler to open/close a SideNav; when animation finishes
	     * report completion in console
	     */
    		function buildToggler(navID) {
      		var debounceFn =  $mdUtil.debounce(function(){
				$mdSidenav(navID)
				.toggle()
				.then(function () {
			 		$log.debug("toggle " + navID + " is done");
				});
          	},100);

      		return debounceFn;
    		}
		//End Main sidenav//

		//AUTH
		$scope.logout = function() {
    			AuthService.logout();
    			$state.go('login');
  		};

  		$scope.user = AuthService.user();
  		$scope.isAuthenticated = AuthService.isAuthenticated();

  		//Listen Events
		$scope.$on(AUTH_EVENTS.notAuthorized, function(event){
			console.log('You are not allowed to access this resource.');
			$state.go('dashboard.profile', {}, {reload: true});
		});

		$scope.$on(AUTH_EVENTS.notAuthenticated, function(event){
			console.log('Sorry, You have to login again.');
			AuthService.logout();
			$state.go('login');
		});

		$scope.$on(AUTH_EVENTS.loginSuccess, function(){
			console.log('Login Succesfully');
			$scope.user = AuthService.user();
  			$scope.isAuthenticated = AuthService.isAuthenticated();
  			var roles = AuthService.user().groups;

  			if (roles.length > 0){
  				switch(roles[0]){
					case 'student': $state.go('dashboard.student', {}, {reload: true}); break;
					case 'teacher': $state.go('dashboard.teacher', {}, {reload: true}); break;
					case 'admin': 	$state.go('dashboard.admin', {}, {reload: true}); break;
					default: 
						$rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
						break;
				}
  			}else{
  				$rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
  			}
  			
		});

		$scope.$on(AUTH_EVENTS.logoutSuccess, function(){
			$scope.user = undefined;
  			$scope.isAuthenticated = false;
		});

		$scope.setCurrentUsername = function(username) {
    			$scope.username = username;
  		};
	})

	/*Login Controller
	Login & Redirect to dashboard
	*/
	.controller('MainMenuCtrl', function ($scope, $timeout, $mdSidenav, $log) {
		var self = this;
		$scope.close = function () {
		 $mdSidenav('mainSideNav').close()
		   .then(function () {
		     $log.debug("close mainSideNav is done");
		   });
		};
	})
	.controller('LoginCtrl', function($scope, $state, AuthService, Validate) {
		//console.log('LoginCtrl');
		$scope.model = {'username':'','password':''};
		$scope.login = function(formData){
			$scope.errors = [];
			Validate.form_validation(formData,$scope.errors);
			if(!formData.$invalid){
				AuthService.login($scope.model.username, $scope.model.password)
				.then(function(response){
						$scope.setCurrentUsername($scope.model.username);
		        	},function(response){
		        		$scope.errors = response;
		        	});
			}
		}
	})

	.controller('ProfileCtrl', function($scope, SCEService) {
		console.log('ProfileCtrl');
		SCEService.UserProfile()
			.then(function(response){
				$scope.profile = response.data;
				//console.log($scope.profile);			
			}, function(response){
				console.log(response)
			});
	})

	.controller('DashCtrl', function($scope, $state, AuthService) {
		console.log("DashCtrl");
		console.log($state.current.data);
	})

	.controller('StudentDashCtrl', function($scope, $state, AuthService, SCEService, $http, SCE_API_URL) {
		console.log("StudentDashCtrl");
		$scope.currentStudent = undefined;
		SCEService.StudentProfile(AuthService.user().username)
		.then(function(response){
			$scope.currentStudent = response.data;
			//console.log($scope.currentStudent);
		});

		//Boleta estudiante
		$scope.schoolyear = null;
		$scope.available_schoolyears = [];
		$scope.selected_schoolyear = undefined;
		$scope.course_enrollments = [];
		
		//Loading entollments 
		$http.get(SCE_API_URL + '/course-enrollments/')
		.then(function(response){
			$scope.course_enrollments = response.data;
			//console.log($scope.course_enrollments);
		});
		
		
		$scope.LoadSchoolYears = function(){
			$http.get(SCE_API_URL + '/school-years/')
			.then(function(response){
				$scope.available_schoolyears = response.data;
			});
		};
	})

	.controller('TeacherDashCtrl', function($scope, $state, SCEService, $log){
		console.log("TeacherDashCtrl");
		$scope.courses = [];

		SCEService.GetCourses([])
		.then(function(response){
			$scope.courses = response.data;
			console.log($scope.courses);
		}, function(){
			console.log('Error');
		})

	});

})()