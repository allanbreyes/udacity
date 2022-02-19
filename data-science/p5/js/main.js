d3.csv("data/data.csv", function(d) {
  var format = d3.time.format("%Y");
  return {
    'Year': format.parse(d.year),
    'Carrier Name': d.carrier_name,
    'On Time': +d.on_time,
    'Arrivals': +d.arrivals
  };
}, function(data) {
  'use strict';

  // append title
  d3.select('#content')
    .append('h2')
    .attr('id', 'title')
    .text('On-Time Arrival Rates for Top U.S. Domestic Airlines, 2003-2014');

  // set svg
  var width = 960,
      height = 640;
  var svg = dimple.newSvg('#content', width, height);
  var myChart = new dimple.chart(svg, data);

  // set y axis
  var minY = 0.5,
      maxY = 1;
  var y = myChart.addMeasureAxis('y', 'On Time');
  y.tickFormat = '%';
  y.overrideMin = minY;
  y.overrideMax = maxY;
  y.title = 'Percentage of Arrivals on Time (within 15 minutes)';

  // set x axis
  var x = myChart.addTimeAxis('x', 'Year');
  x.tickFormat = '%Y';
  x.title = 'Year';

  // set series and legend
  var s = myChart.addSeries('Carrier Name', dimple.plot.scatter);
  var p = myChart.addSeries('Carrier Name', dimple.plot.line);
  var legend = myChart.addLegend(width*0.65, 60, width*0.25, 60, 'right');

  // draw
  myChart.draw();

  // handle mouse events on gridlines
  y.gridlineShapes.selectAll('line')
    .style('opacity', 0.25)
    .on('mouseover', function(e) {
      d3.select(this)
        .style('opacity', 1);
    }).on('mouseleave', function(e) {
      d3.select(this)
        .style('opacity', 0.25);
    });

  // handle mouse events on paths
  d3.selectAll('path')
    .style('opacity', 0.25)
    .on('mouseover', function(e) {
      d3.select(this)
        .style('stroke-width', '8px')
        .style('opacity', 1)
        .attr('z-index', '1');
  }).on('mouseleave', function(e) {
      d3.select(this)
        .style('stroke-width', '2px')
        .style('opacity', 0.25)
        .attr('z-index', '0');
  });
});
