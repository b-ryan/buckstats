angular.module('stand', ['ngResource'])

  .factory('Event', function($resource) {
    return $resource(
      '/events'
    );
  })

  ;

var StandCtrl = function($scope, $http, Event) {

  $scope.events = Event.query();

  $scope.standing = function() {
    console.log("standing...");
    $http
      .post('/stand')
      .success(function(response) {
        console.log('worked!');
        $scope.events.$get();
      });
  };

  $scope.sitting = function() {
    console.log("sitting...");
    $http
      .post('/sit')
      .success(function(response) {
        console.log('worked!');
        $scope.events.$get();
      });
  };
};
