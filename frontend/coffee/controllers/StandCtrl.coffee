SUNDAY = 0
MONDAY = 1

createBaseChart = () ->
  chart:
    zoomType: 'x'
    spacingRight: 20
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

  # ##########################################################################
  # MAIN CHART

  createMainChart = () ->
    base = createBaseChart()
    base.title = { text: "Buck's weight" }
    base.navigator = { enabled: true }
    base.series = [
      {
        name: 'Weight',
        data: [],
        marker: { enabled: false },
        id: 'dataseries'
      }
      {
        name: 'Goal weight',
        data: [],
        marker: { enabled: false },
        color: '#ffc9c9'
      }
      {
        name: 'Moving average',
        data: [],
        marker: { enabled: false },
        color: '#666', visible: false
      }
      {
        name: 'notes',
        data: [],
        type: 'flags',
        onSeries: 'dataseries'
      }
    ]
    return base

  $scope.mainChart = createMainChart()

  calculateMovingAverages = (weights) ->

    series = []

    for i in [2...(weights.length - 2)]
      row = [new Date(weights[i].date).getTime(), 0]

      for j in [-2..2]
        row[1] += weights[i + j].weight / 5.0

      series.push row

    return series

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
    $scope.mainChart.series[2].data = calculateMovingAverages(weights)
    $scope.mainChart.series[3].data = notesData

  $scope.refreshMainChart = () ->
    $scope.weights = Weight.query q:
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
    , addSeriesToMainChart

  # ##########################################################################
  # WEEK OVER WEEK CHART

  NUM_WEEKS = 4

  $scope.weekOverWeekChart = createBaseChart()
  $scope.weekOverWeekChart.title = { text: 'Week over week' }
  $scope.weekOverWeekChart.series = [
    { name: 'Three weeks ago', data: [], marker: { enabled: false } }
    { name: 'Two weeks ago', data: [], marker: { enabled: false } }
    { name: 'Last week', data: [], marker: { enabled: false } }
    { name: 'This week', data: [], marker: { enabled: false } }
  ]

  lastStartOfWeek = (weekStartDay) ->
    d = new Date()
    d.setHours 0
    d.setMinutes 0
    d.setSeconds 0

    dayOfWeek = d.getDay()
    d.setDate(d.getDate() - dayOfWeek + weekStartDay)

    return d

  modifyWeek = (startOfWeek, offset) ->
    d = new Date(startOfWeek.getTime())
    d.setDate(d.getDate() + offset)
    return d

  previousWeek = (startOfWeek) ->
    modifyWeek startOfWeek, -7

  nextWeek = (startOfWeek) ->
    modifyWeek startOfWeek, 7

  fmt = (date) ->
    date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()

  queryWeightsForWeek = (startOfWeek) ->
    q = Weight.query q:
      filters: [
        {
          name: 'date'
          op: '>='
          val: fmt(startOfWeek)
        }
        {
          name: 'date'
          op: '<'
          val: fmt(nextWeek(startOfWeek))
        }
      ]
      order_by: [
        {
          field: 'date'
          direction: 'asc'
        }
      ]
    return q.$promise

  $scope.refreshWoWChart = () ->
    sunday = lastStartOfWeek(SUNDAY)
    weekStarts = (modifyWeek(sunday, i * -7) for i in [(NUM_WEEKS-1)..0])

    promises = (queryWeightsForWeek(j) for j in weekStarts)

    $q.all(promises).then (data) ->
      for weights, index in data
        seriesData = (w.weight for w in weights)
        $scope.weekOverWeekChart.series[index].data = seriesData

  $scope.refreshWeights = () ->
    $scope.refreshing = true

    $http.post('/api/weights/refresh').success () ->
      $scope.refreshing = false
      $scope.refreshMainChart()
      $scope.refreshWoWChart()

  $scope.refreshMainChart()
  $scope.refreshWoWChart()
