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

MONDAY = 1

latestMonday = () ->
  d = new Date()
  d.setHours 0
  d.setMinutes 0
  d.setSeconds 0

  dayOfWeek = d.getDay()
  if dayOfWeek != MONDAY
    d.setDate(d.getDate() - dayOfWeek + MONDAY)

  return d

buckstats.controller 'StandCtrl', ($scope, $q, Weight) ->

  createBaseChart = () ->
    useHighStocks: true
    loading: true
    options:
      chart: { zoomType: 'x', spacingRight: 20 }
      tooltip: { shared: true }
      rangeSelector: { buttons: [
          { type: 'week', count: 1, text: '1w' }
          { type: 'week', count: 2, text: '2w' }
          { type: 'month', count: 1, text: '1m' }
          { type: 'month', count: 3, text: '3m' }
          { type: 'all', text: 'All' }
        ]}
    xAxis:
      type: 'datetime'
      tickInterval: 7 * 24 * 60 * 60 * 1000 # one week
      gridLineWidth: 1
    yAxis:
      title: { text: 'Weight (lbs)' }
      opposite: true
    series: []

  $scope.chart = createBaseChart()
  $scope.chart.title = { text: "Buck's weight" }

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

    $scope.chart.series.push
      name: 'Weight'
      data: weightData
      id: 'dataseries'

    $scope.chart.series.push
      name: 'Goal weight'
      data: goalData
      marker:
        enabled: false
      color: '#ffc9c9'

    $scope.chart.series.push
      name: 'notes'
      type: 'flags'
      data: notesData
      onSeries: 'dataseries'

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
