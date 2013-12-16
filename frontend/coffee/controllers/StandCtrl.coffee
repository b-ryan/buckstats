SUNDAY = 0

latestSunday = () ->
  d = new Date()
  d.setHours 0
  d.setMinutes 0
  d.setSeconds 0

  dayOfWeek = d.getDay()
  if dayOfWeek != SUNDAY
    d.setDate(d.getDate() - dayOfWeek + SUNDAY)

  return d

createBaseChart = () ->
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
    base.title = { text: "Buck's weight" }
    base.series = [
      { name: 'Weight',      data: [], marker: { enabled: false }, id: 'dataseries' }
      { name: 'Goal weight', data: [], marker: { enabled: false }, color: '#ffc9c9' }
      { name: 'notes',       data: [], type: 'flags', onSeries: 'dataseries' }
    ]
    return base

  $scope.mainChart = createMainChart()

  addSeriesToMainChart = (weights) ->
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

    $scope.mainChart.series[0].data = weightData
    $scope.mainChart.series[1].data = goalData
    $scope.mainChart.series[2].data = notesData

  $scope.refreshMainChart = () ->
    $scope.weights = Weight.query
      q:
        order_by: [
          {
            field: 'date'
            direction: 'asc'
          }
        ]
      , addSeriesToMainChart

  $scope.refreshWeights = () ->
    $scope.refreshing = true

    $http.post('/api/weights/refresh').success () ->
      $scope.refreshing = false
      $scope.refreshMainChart()

  $scope.refreshMainChart()


  sunday = latestSunday()
  console.log sunday

  fmt = (date) ->
    date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()

  $scope.w1 = Weight.query
    q:
      filters: [
        {
          name: 'date'
          op: '>='
          val: fmt(sunday)
        }
      ]
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
  , (weights) ->
    data = [new Date(w.date).getTime(), w.weight] for w in weights

    console.log weights
    console.log data

    $scope.weekOverWeekChart = createBaseChart()
    $scope.weekOverWeekChart.title = { text: 'Week over week' }
    $scope.weekOverWeekChart.series = [
      { name: 'This week', data: data, marker: { enabled: false } }
    ]
