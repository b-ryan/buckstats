stand = angular.module 'stand', ['ngResource']
window.stand = stand

RESOURCE_ACTIONS =
  query:
    method: 'GET'
    transformResponse: (data) ->
      angular.fromJson(data).objects
    isArray: true
  update:
    method: 'PUT'
    params: {id: '@id'}
  delete:
    method: 'DELETE'
    params: {id: '@id'}

stand.factory 'Weight', ($resource) ->
  $resource '/api/weights/:id', {}, RESOURCE_ACTIONS

window.StandCtrl = ($scope, Weight) ->

  $scope.weights = Weight.query()
