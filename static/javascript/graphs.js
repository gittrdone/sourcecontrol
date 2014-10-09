var data = [];

var author_list = document.getElementById("json_authors").innerHTML;
var parsed_list = JSON.parse(author_list, "fields");
for (i = 0; i < parsed_list.length; i ++) {
    var author_name = parsed_list[i].fields.name;
    var num_commits = parsed_list[i].fields.num_commits;
    var author = {
        name:author_name,
        commits:num_commits
    };
    data.push(author);
}

var width = 400,
    height = 400,
    radius = Math.min(width, height) / 2,
    labelr = radius + 30, // radius for label anchor
    color = d3.scale.category20(),
    donut = d3.layout.pie(),
    arc = d3.svg.arc().innerRadius(0).outerRadius(radius);

var vis = d3.select("#pie_chart")
  .append("svg:svg")
    .data([data])
    .attr("width", width + 300)
    .attr("height", height + 150)
    .style("margin", "auto");

var arcs = vis.selectAll("g.arc")
    .data(donut.value(function(d) { return d.commits }))
  .enter().append("svg:g")
    .attr("class", "arc")
    .attr("transform", "translate(" + (radius + 150) + "," + (radius + 50) + ")");

arcs.append("svg:path")
    .attr("fill", function(d, i) { return color(i); })
    .attr("d", arc);

arcs.append("svg:text")
    .attr("transform", function(d) {
        var c = arc.centroid(d),
            x = c[0],
            y = c[1],
            // pythagorean theorem for hypotenuse
            h = Math.sqrt(x*x + y*y);
        return "translate(" + (x/h * labelr) +  ',' +
           (y/h * labelr) +  ")";
    })
    .attr("dy", ".35em")
    .attr("text-anchor", function(d) {
        // are we past the center?

        return (d.endAngle + d.startAngle)/2 > Math.PI ?
            "end" : "start";
    })

    .attr("display", function(d) {
        if((d.endAngle - d.startAngle) > 0.1) {
            return "normal"
        }

        else {
            return "none"
        }
    })
    .text(function(d, i) { return d.data.name; });

data = [];
var week_commit_list = document.getElementById("week_commits").innerHTML;
var week_commit_json = JSON.parse(week_commit_list);
var keys = Object.keys(week_commit_json);

for (i = 0; i < keys.length; i ++) {
    var day = keys[i];
    var num_commits = week_commit_json[day];
    var dayData = {
        day:parseInt(day),
        commits:num_commits
    };
    data.push(dayData);
}

var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("#bar_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

  x.domain(data.map(function(d) { return d.day; }));
  y.domain([0, d3.max(data, function(d) { return d.commits; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" )

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("# Commits");

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) {return x(d.day); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.commits); })
      .attr("height", function(d) { return height - y(d.commits); });
