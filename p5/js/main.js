d3.csv("data/data.csv", function(d) {
  var format = d3.time.format("%Y");
  return {
    year: format.parse(d.year),
    carrier_name: d.carrier_name,
    on_time: +d.on_time,
    arrivals: +d.arrivals
  };
}, function(data) {
  'use strict';

  d3.select('#content')
    .append('h2')
    .attr('id', 'title')
    .text('On-Time Arrival Rates for Top U.S. Domestic Airlines, 2003-2014');

  var width = 960,
      height = 640;

  var svg = dimple.newSvg('#content', 960, 640);
  var myChart = new dimple.chart(svg, data);

  // set y axis limits
  var minY = 0.5,
      maxY = 1;

  // set x axis
  var x = myChart.addTimeAxis('x', 'year');
  x.tickFormat = '%Y';
  x.title = 'Year';

  // set y axis
  var y = myChart.addMeasureAxis('y', 'on_time');
  y.tickFormat = '%';
  y.overrideMin = minY;
  y.overrideMax = maxY;
  y.title = 'Percentage of Arrivals on Time (within 15 minutes)';
  myChart.addSeries('carrier_name', dimple.plot.line);
  var s = myChart.addSeries('carrier_name', dimple.plot.scatter);
  var legend = myChart.addLegend(width*0.65, 60, width*0.25, 60, 'right');

  // handle hover events
  // s.addEventHandler('mouseover', onHover);
  // s.addEventHandler('mouseleave', onLeave);

  myChart.draw();
});

$('.dimple-series-1').on('mouseover', function() {
  console.log('hello!');
  self.style('display: none');
});

function onHover(e) {
  console.log(e);
}
function onLeave(e) {
  console.log(e.selectedShape);
}