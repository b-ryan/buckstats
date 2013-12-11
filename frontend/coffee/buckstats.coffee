buckstats = angular.module 'buckstats', ['ngResource', 'highcharts-ng']
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

window.StandCtrl = ($scope, Weight) ->

  $scope.chart =
    useHighStocks: true
    loading: true
    options:
      chart:
        zoomType: 'x'
        spacingRight: 20
      tooltip:
        shared: true
      rangeSelector:
        buttons: [
          {
            type: 'week'
            count: 1
            text: '1w'
          }
          {
            type: 'week'
            count: 2
            text: '2w'
          }
          {
            type: 'month'
            count: 1
            text: '1m'
          }
          {
            type: 'month'
            count: 3
            text: '3m'
          }
          {
            type: 'all'
            text: 'All'
          }
        ]
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
        name: 'Weight'
        data: []
        id: 'dataseries'
      }
      {
        name: 'Goal weight'
        data: []
        marker:
          enabled: false
        color: '#ffc9c9'
      }
      {
        name: 'notes'
        type: 'flags'
        data: []
        onSeries: 'dataseries'
      }
    ]

  addWeightsToChart = (weights) ->
    weightData = []
    goalData = []
    notesData = []

    for w in weights
      t = new Date(w.date).getTime()
      weightData.push [t, w.weight]

      if w.goal_weight
        goalData.push [t, w.goal_weight]

      if w.notes
        notesData.push
          x: t
          title: '✔'
          text: w.notes

    $scope.chart.series[0].data = weightData
    $scope.chart.series[1].data = goalData
    $scope.chart.series[2].data = notesData

    $scope.chart.loading = false
    $scope.chart.options.navigator =
      enabled: true

  $scope.weights = Weight.query
    q:
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
    , addWeightsToChart
