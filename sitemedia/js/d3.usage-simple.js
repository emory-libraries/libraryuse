var data = [{"prsn_e_type__count": 8919, "prsn_e_type": "Student"}, {"prsn_e_type__count": 4411, "prsn_e_type": "Student/Staff"}, {"prsn_e_type__count": 2082, "prsn_e_type": "Staff"}, {"prsn_e_type__count": 1977, "prsn_e_type": "Faculty"}, {"prsn_e_type__count": 270, "prsn_e_type": "Staff/Student"}, {"prsn_e_type__count": 86, "prsn_e_type": "Sponsored"}, {"prsn_e_type__count": 55, "prsn_e_type": "Retired"}, {"prsn_e_type__count": 54, "prsn_e_type": "Pre-start"}, {"prsn_e_type__count": 43, "prsn_e_type": "Unknown"}, {"prsn_e_type__count": 11, "prsn_e_type": "Administrative"}]
//var data = d3.json("http://localhost:4242/usage/prsntype");

var margin = {top: 20, right: 20, bottom: 60, left: 60},
    width = 900 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var svg = d3.select("#chart2").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


  data.forEach(function(d) {
    d.prsn_e_type__count = +d.prsn_e_type__count;
  });

  x.domain(data.map(function(d) { return d.prsn_e_type; }));
  y.domain([0, d3.max(data, function(d) { return d.prsn_e_type__count; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
  	.append("text")
  	  .attr("x",20)
  	  .attr("y",40)
  	  .text("Person Type (prsn_e_type)");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("x",-10)
      .style("text-anchor", "end")
      .text("Visits");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.prsn_e_type); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.prsn_e_type__count); })
      .attr("height", function(d) { return height - y(d.prsn_e_type__count); });
