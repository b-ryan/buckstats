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
    options:
      chart:
        type: 'line'
        zoomType: 'x'
        spacingRight: 20
      tooltip:
        shared: true
    loading: true
    title:
      text: "Buck's weight"
    xAxis:
      type: 'datetime'
      tickInterval: 7 * 24 * 60 * 60 * 1000 # one week
      gridLineWidth: 1
    yAxis:
      title:
        text: 'Weight (lbs)'
      opposite: true
    series: [
      {
        name: 'Goal weight'
        data: []
        marker:
          radius: 0
        color: 'red'
      }
      {
        name: 'Weight'
        data: []
      }
    ]

  addWeightsToChart = (weights) ->
    goalData = []
    weightData = []

    for w in weights
      t = new Date(w.date).getTime()
      goalData.push [t, w.goal_weight]
      weightData.push [t, w.weight]

    $scope.chart.series[0].data = goalData
    $scope.chart.series[1].data = weightData

    $scope.chart.loading = false

  $scope.weights = Weight.query
    q:
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
    , addWeightsToChart
