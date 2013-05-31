var ONE_SECOND = 1000;
var ONE_MINUTE = 60 * ONE_SECOND;
var ONE_HOUR = 60 * ONE_MINUTE;

angular.module('stand', ['ngResource'])

  .filter('event_duration', function() {
    return function(event) {
      var start = (new Date(event.start_time)).getTime();
      var end = (new Date(event.end_time)).getTime();
      if(!end)
        return 'ongoing...';

      var diff = end - start;
      var result = '';

      var hours = Math.floor(diff / ONE_HOUR);
      var minutes = Math.floor((diff % ONE_HOUR) / ONE_MINUTE);
      var seconds = Math.floor((diff % ONE_MINUTE) / ONE_SECOND);
      result += hours + ' hours, ';
      result += minutes + ' minutes, ';
      result += seconds + ' seconds';

      return result;
    };
  })

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
