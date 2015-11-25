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
			console.log(event)
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
					case 'student':
						$state.go('dashboard.student', {}, {reload: true}); break;
					case 'teacher':
						$state.go('dashboard.teacher', {}, {reload: true}); break;
					case 'administrator':
						$state.go('dashboard.administrator', {}, {reload: true}); break;
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
	.controller('MainMenuCtrl', function ($scope, $timeout, $mdSidenav, $log, AuthService) {
		var self = this;
		$scope.role = AuthService.getCurrentRole();//'administrator'
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

	.controller('StudentDashCtrl', function($scope, $state, AuthService, SCEService, $http, API_URL) {
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
		
		//Loading enrollments
		$http.get(API_URL + '/sce/course-enrollments/')
		.then(function(response){
			$scope.course_enrollments = response.data;
			//console.log($scope.course_enrollments);
		});
		
		
		$scope.LoadSchoolYears = function(){
			$http.get(API_URL + '/sce/school-years/')
			.then(function(response){
				$scope.available_schoolyears = response.data;
			});
		};



		//Edit a course enrollment
		//var sample_course_enrollment = undefined;
		//var get_sample_course_enrollment =
		//$http.get('http://localhost:8000/api/sce/course-enrollments/1/');
		//get_sample_course_enrollment.then(function(response){
		//	sample_course_enrollment = response.data;
		//	console.log(sample_course_enrollment);
		//	//Modify the course enrollments
		//	sample_course_enrollment.scores[0].score = "10.0";
		//	sample_course_enrollment.scores[1].score = "10.0";
		//	sample_course_enrollment.scores[2].score = "10.0";
		//	var put_sample_course_enrollment = $http.put(
		//		'http://localhost:8000/api/sce/course-enrollments/1/',
		//		{
		//			student: sample_course_enrollment.student,
		//			course: sample_course_enrollment.course,
		//			scores: sample_course_enrollment.scores
		//		}
		//	);
		//	put_sample_course_enrollment.then(function(response){
		//		console.log(response);
		//	})
        //
		//}, function(response){
		//	console.log("Some Error");
		//});





	})

	.controller('TeacherDashCtrl', function($scope, $state, SCEService, $log, $http, API_URL) {
		console.log('TeacherDashCtrl');
		$scope.courses = [];

		var get_courses = SCEService.GetCourses([]);
		get_courses.then(function(response){
			$scope.courses = response.data;
		}, function(){
			console.log('Error');
		});

		////Edit a course enrollment
		//var sample_course_enrollment = undefined;
		//var get_sample_course_enrollment =
		//$http.get('http://localhost:8000/api/sce/course-enrollments/1/');
		//get_sample_course_enrollment.then(function(response){
		//	sample_course_enrollment = response.data;
		//	console.log(sample_course_enrollment);
		//	//Modify the course enrollments
		//	sample_course_enrollment.scores[0].score = "9.8";
		//	sample_course_enrollment.scores[1].score = "9.7";
		//	sample_course_enrollment.scores[2].score = "9.6";
		//	var put_sample_course_enrollment = $http.put(
		//		'http://localhost:8000/api/sce/course-enrollments/1/',
		//		{
		//			student: sample_course_enrollment.student,
		//			course: sample_course_enrollment.course,
		//			scores: sample_course_enrollment.scores
		//		}
		//	);
		//	put_sample_course_enrollment.then(function(response){
		//		console.log(response);
		//	})
        //
		//}, function(response){
		//	console.log("Some Error");
		//});

			//Create multiple Courses
			var params = [
				{school_year_id:1, subject_id:11, cohort_id: 10},
				{school_year_id:1, subject_id:11, cohort_id: 11}
			];
			var post = $http.post(API_URL + '/sce/courses/', params);
			post.then(function(response){
				console.log(response);
			}, function(response){
				console.log(response);
			})
	})

	.controller('AdministratorCtrl', function($scope, SCEService, $mdDialog){
		//School Year Module
		//Initial values

	})
	.controller('AdminSchoolYearCtrl', function($scope, SCEService){
		$scope.school_years = [];
		$scope.educative_programs = [];
		$scope.school_year_to_create = {
			name: undefined,
			start_date: undefined,
			end_date: undefined,
			educative_program_id: undefined,
		};
		$scope.LoadEducativePrograms = function(){
			SCEService.GetEducativePrograms().then(function(response){
				$scope.educative_programs = response.data.results;
			}, function(){
				console.log("Some error at GetEducativePrograms()")
			});
		};

		$scope.ActivateSchoolYear = function(school_year){
			SCEService.ActivateSchoolYear(school_year.id).then(function(response){
				school_year.is_active = response.data.result.is_active;
			}, function (response) {
				console.log(response)
			});
		};
		$scope.DeactivateSchoolYear = function(school_year){
			SCEService.DeactivateSchoolYear(school_year.id).then(function(response){
				school_year.is_active = response.data.result.is_active;
			}, function (response) {
				console.log(response)
			});
		};
		$scope.CreateCoursesBySchoolYear = function(school_year, complete_courses){
			SCEService.CreateCoursesBySchoolYear(school_year.id, complete_courses).then(function(response){
				console.log(response.data);
			}, function (response) {
				console.log(response)
			});
		};

	 	//Run initial services
		SCEService.GetSchoolYears().then(function(response){
			$scope.school_years = response.data.results;
		}, function(error){
			$console.log("Error at Retrieve School Years");
		});
	})
	.controller('AdminEditSchoolYearCtrl', function(){
	})
	.controller('AdminCreateSchoolYearCtrl', function($scope, SCEService, $state){
		$scope.school_year = {
			start_date: undefined,
			end_date: undefined,
			educative_program_id: undefined
		};

		$scope.CreateSchoolYear = function(formData){
			$scope.errors = [];
			SCEService.CreateSchoolYear(
					$scope.school_year.start_date.toISOString().slice(0,10),
					$scope.school_year.end_date.toISOString().slice(0,10),
					$scope.school_year.educative_program_id
			).then(function(response){
				$scope.$parent.school_years.push(response.data);
				$state.go('dashboard.administrator.school_years')
			}, function(response){
				console.log(response);
			});
		}
	})
	.controller('AdminEducativeProgramsCtrl', function($scope, SCEService){
		var self = this;
		self.educative_programs = [];
		SCEService.GetEducativePrograms().then(function(response){
			self.educative_programs = response.data.results;
		}, function(response){
			console.log(response)
		});
	});
})()