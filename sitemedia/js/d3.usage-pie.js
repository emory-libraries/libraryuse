//var data = d3.json("http://localhost:4242/usage/prsntype");
//var data_1 = [{"count": 8919, "name": "Student"}, {"count": 2082, "name": "Staff"}, {"count": 1977, "name": "Faculty"}, {"count": 886, "name": "Administrative"}, ]
//var data_2 = [{"count": 6919, "name": "Student"}, {"count": 4082, "name": "Staff"}, {"count": 2977, "name": "Faculty"}, {"count": 886, "name": "Administrative"}, ]


var width = 960,
    height = 500,
    radius = Math.min(width, height) / 2;

var color = d3.scale.category20();

var pie = d3.layout.pie()
    .value(function(d) { return d.department; })
    .sort(null);

var arc = d3.svg.arc()
    .innerRadius(0)
    .outerRadius(radius - 20);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

d3.tsv("/static/data/data.tsv", type, function(error, data) {
  var path = svg.datum(data).selectAll("path")
      .data(pie)
    .enter().append("path")
      .attr("fill", function(d, i) { return color(i); })
      .attr("d", arc)
      .each(function(d) { this._current = d; }); // store the initial angles

  d3.selectAll("input")
      .on("change", change);

  var timeout = setTimeout(function() {
    d3.select("input[value=\"division\"]").property("checked", true).each(change);
  }, 2000);

  function change() {
    var value = this.value;
    clearTimeout(timeout);
    pie.value(function(d) { return d[value]; }); // change the value function
    path = path.data(pie); // compute the new angles
    path.transition().duration(750).attrTween("d", arcTween); // redraw the arcs
  }
});

function type(d) {
  d.department = +d.department;
  d.division = +d.division;
  d.person_type = +d.person_type;
  d.status = +d.status;
  return d;
}

// Store the displayed angles in _current.
// Then, interpolate from _current to the new angles.
// During the transition, _current is updated in-place by d3.interpolate.
function arcTween(a) {
  var i = d3.interpolate(this._current, a);
  this._current = i(0);
  return function(t) {
    return arc(i(t));
  };
}