buckstats = angular.module 'buckstats', ['ngResource']
window.buckstats = buckstats

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

buckstats.factory 'Weight', ($resource) ->
  $resource '/api/weights/:id', {}, RESOURCE_ACTIONS
