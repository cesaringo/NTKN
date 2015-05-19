'use strict';

angular.module('ntkn.authentication.controllers')
  .controller('MainController', function ($scope, $cookies, $location, Authentication) {
    
    $scope.login = function(){
      Authentication.login(prompt('Username'),prompt('password'))
      .then(function(data){
        handleSuccess(data);
      },handleError);
    }
    
    $scope.logout = function(){
      Authentication.logout()
      .then(handleSuccess,handleError);
    }
    
    $scope.resetPassword = function(){
      Authentication.resetPassword(prompt('Email'))
      .then(handleSuccess,handleError);
    }
    
    $scope.register = function(){
      Authentication.register(prompt('Username'),prompt('Password'),prompt('Email'))
      .then(handleSuccess,handleError);
    }
    
    $scope.verify = function(){
      Authentication.verify(prompt("Please enter verification code"))
      .then(handleSuccess,handleError);
    }
    
    $scope.goVerify = function(){
      $location.path("/verifyEmail/"+prompt("Please enter verification code"));
    }
    
    $scope.changePassword = function(){
      Authentication.changePassword(prompt("Password"), prompt("Repeat Password"))
      .then(handleSuccess,handleError);
    }
    
    $scope.profile = function(){
      Authentication.profile()
      .then(handleSuccess,handleError);
    }
    
    $scope.updateProfile = function(){
      Authentication.updateProfile({'first_name': prompt("First Name"), 'last_name': prompt("Last Name"), 'email': prompt("Email")})
      .then(handleSuccess,handleError);
    }
    
    $scope.confirmReset = function(){
      Authentication.confirmReset(prompt("Code 1"), prompt("Code 2"), prompt("Password"), prompt("Repeat Password"))
      .then(handleSuccess,handleError);
    }

    $scope.goConfirmReset = function(){
      $location.path("/passwordResetConfirm/"+prompt("Code 1")+"/"+prompt("Code 2"))
    }
    
    var handleSuccess = function(data){
      $scope.response = data;
    }
    
    var handleError = function(data){
      $scope.response = data;
    }

    $scope.show_login = true;
    $scope.$on("Authentication.logged_in", function(data){
      $scope.show_login = false;
    });
    $scope.$on("Authentication.logged_out", function(data){
      $scope.show_login = true;
    });

  });