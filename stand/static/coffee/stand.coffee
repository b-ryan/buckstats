stand = angular.module 'stand', ['ngResource', 'highcharts-ng']
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

  $scope.chart =
    chart:
      zoomType: 'x'
      spacingRight: 20
    title:
      text: 'my friendly chart'
    xAxis:
      type: 'datetime'
      title:
        text: null
    yAxis:
      title:
        text: 'Weight (lbs)'
    series: [
      {
        name: 'Weight'
        data: []
      }
    ]
    options:
      chart:
        type: 'line'

  addWeightsToChart = (weights) ->
    data = []

    for w in weights
      data.push [new Date(w.date).getTime(), w.weight]

    $scope.chart.series[0].data = data

  $scope.weights = Weight.query
    q:
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
    , addWeightsToChart
