var data = [];

var author_list = document.getElementById("jsonAuthors").innerHTML;
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
        console.log(d.endAngle - d.startAngle);
        console.log("anus");
        if((d.endAngle - d.startAngle) > 0.1) {
            console.log("including");
            return "normal"
        }

        else {
            console.log("not including");
            return "none"
        }
    })
    .text(function(d, i) { return d.data.name; });