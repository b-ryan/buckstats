angular.module('stand', ['ngResource'])

  .factory('Event', function($resource) {
    return $resource(
      '/latest'
    );
  })

  ;

var StandCtrl = function($scope, $http, Event) {

  $scope.latest = Event.get();

  $scope.standing = function() {
    console.log("standing...");
    $http
      .post('/stand')
      .success(function(response) {
        console.log('worked!');
        $scope.latest.$get();
      });
  };

  $scope.sitting = function() {
    console.log("sitting...");
    $http
      .post('/sit')
      .success(function(response) {
        console.log('worked!');
        $scope.latest.$get();
      });
  };
};
