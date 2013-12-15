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

createBaseChart = () ->
  loading: true
  chart:
    zoomType: 'x'
    spacingRight: 20
  navigator: { enabled: true }
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

buckstats.controller 'StandCtrl', ($scope, $q, $http, Weight) ->

  createMainChart = () ->
    base = createBaseChart()
    base.series = [
      { name: 'Weight',      data: [], marker: { enabled: false }, id: 'dataseries' }
      { name: 'Goal weight', data: [], marker: { enabled: false }, color: '#ffc9c9' }
      { name: 'notes',       data: [], type: 'flags', onSeries: 'dataseries' }
    ]
    base.chart.title = { text: "Buck's weight" }
    return base

  $scope.chart = createMainChart()

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

  $scope.refresh = () ->
    $scope.weights = Weight.query
      q:
        order_by: [
          {
            field: 'date'
            direction: 'asc'
          }
        ]
      , addWeightsToChart

  $scope.refreshWeights = () ->
    $http.post('/api/weights/refresh').success () ->
      $scope.refresh()

  $scope.refresh()
