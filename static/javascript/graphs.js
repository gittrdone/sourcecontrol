var data = [];

var parsed_list = parsedAuthorData; //Get data from script tag on repoDetail.html
for (i = 0; i < parsed_list.length; i ++) {
    var author_name = parsed_list[i].fields.name;
    var num_commits = parsed_list[i].fields.num_commits;
    var author = {
        name:author_name,
        commits:num_commits
    };
    data.push(author);
}

var width = 200, //Specify height and width of div chart is placed in (not the pie itself)
    height = 200,
    radius = Math.min(width, height) / 2, //set the radius of the pie
    labelr = radius + 30, // radius for label anchor
    color = d3.scale.category20b(), //set the color scheme APPARENTLY THIS SHIT IS BLACK MAGIC
    donut = d3.layout.pie(), //Specify type of d3 chart
    arc = d3.svg.arc().innerRadius(0).outerRadius(radius); //Specifies radii (if you set a non-zero value for innerRadius
//, it makes it a donut. Idk why you'd want a donut chart as opposed to the clearly superior pie format.

//Appends a new svg (the pie) to the div that I made ahead of time
var vis = d3.select("#pie_chart")
  .append("svg:svg")
    .data([data]) //Says what data it should be processing
    .attr("width", width + 300)
    .attr("height", height + 150)
    .style("margin", "auto"); //center

var arcs = vis.selectAll("g.arc") //Uses the data to draw the slices (called arcs)
    .data(donut.value(function(d) { return d.commits })) //Black magic
  .enter().append("svg:g") //Append arcs to the chart
    .attr("class", "arc")
    .attr("transform", "translate(" + (radius + 150) + "," + (radius + 90) + ")"); //Moves shit to the left
    // and right before appending it

//Changes the color of the arc
arcs.append("svg:path")
    .attr("fill", function(d, i) { return color(i); })
    .attr("d", arc);

//Adds text labels on the outside of the donut
arcs.append("svg:text")
    .attr("transform", function(d) {
        var c = arc.centroid(d), //Get center of donut
            x = c[0],
            y = c[1],
            // pythagorean theorem for hypotenuse
            h = Math.sqrt(x*x + y*y);
        return "translate(" + (x/h * labelr) +  ',' +
           (y/h * labelr) +  ")";
    })
    .attr("dy", "0.5em")
    .attr("text-anchor", function(d) {
        // are we past the center?

        return (d.endAngle + d.startAngle)/2 > Math.PI ?
            "end" : "start";
    })

    .attr("display", function(d) { //Don't display label if the slice is REALLY SMALL
        if((d.endAngle - d.startAngle) > 0.1) {
            return "normal"
        }

        else {
            return "none"
        }
    })
    .style("font-size", "12px")
    .text(function(d, i) { return d.data.name; });

//Append title
arcs.append("svg:text")
    .attr("x", 0)
    .attr("y", -150)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("font-weight", "bold")
    .text("Commits per Author");


//ITS BAR CHART TIME
//Parse data into JSON
data = [];
var week_commit_json = parsedWeekData; //Get data from script tag on repoDetail.html
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

var margin = {top: 70, right: 20, bottom: 70, left: 40},
    width = 400 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

var x = d3.scale.ordinal().rangeRoundBands([0, width], .09);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(5);

var svg = d3.select("#bar_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("font-size", "12px")
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

  x.domain(data.map(function(d) { return d.day; }));
  y.domain([0, d3.max(data, function(d) { return d.commits; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("transform", "rotate(0)")
      .attr("y", 35)
      .attr("x", 300)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .style("font-size", "14px")
      .text("Day of month")
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .style("font-size", "14px")
      .text("# Commits");

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) {return x(d.day); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.commits); })
      .attr("height", function(d) { return height - y(d.commits); });

  svg.append("svg:text")
      .attr("x", (width / 2))
      .attr("y", 5 - (margin.top / 2))
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Commits over Week");
