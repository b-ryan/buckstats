## Adapted from https://github.com/rootux/angular-highcharts-directive

buckstats.directive 'highchart', () ->
  restrict: 'E'
  template: '<div></div>'
  scope:
    chartData: "=value"
  transclude:true
  replace: true

  link: (scope, element, attrs) ->
    chartsDefaults =
      chart:
        renderTo: element[0]
        type: attrs.type or null
        height: attrs.height or null
        width: attrs.width or null

    update = (value) ->
      if(!value)
        return

      deepCopy = true
      newSettings = {}
      $.extend deepCopy, newSettings, chartsDefaults, scope.chartData

      chart = new Highcharts.Chart(newSettings)

    scope.$watch 'chartData', update, true

