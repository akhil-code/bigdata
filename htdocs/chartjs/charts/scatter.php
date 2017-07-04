<?php
  $filename = "..\\..\\config\\plotData.txt";
  $lines = getLines($filename);
  $data = array();
  for($x=2;$x<count($lines);$x++){
    $temp = explode(":",$lines[$x]);
    $data[$temp[0]] = $temp[1];
  }
  $values = $data['values'];
  $title = $data['title'];
  $xtitle = $data['xtitle'];
  $ytitle = $data['ytitle'];
  function getLines($filename){
    $myfile = fopen($filename,"r");
    $txt = fread($myfile,filesize($filename));
    $lines = explode(PHP_EOL,$txt);
    fclose($myfile);
    return $lines;
  }
?>

<!DOCTYPE html>
    <html>
      <head>
        <title>Scatter Plot</title>
 <style>
  .chart {
     }
 point{
 r:2;
 }
   .main text {
      font: 10px sans-serif;
      }
  .axis line,
  .axis path {
    shape-rendering: crispEdges;
    stroke: black;
    fill: none;
   }
  circle {
  shape-rendering: crispEdges;
  fill: steelblue;
  stroke: black;
    }
</style>
<!-- <script type="text/javascript" src="http://mbostock.github.com/d3/d3.js"></script> -->
<script type="text/javascript" src="http://d3js.org/d3.v2.js"></script>

 </head>
<body>
 <script>
  var data = <?php echo $values; ?>;
  var xtitle = "<?php echo $xtitle; ?>";
  var ytitle = "<?php echo $ytitle; ?>";
  var title = "<?php echo $title; ?> ";
  var margin = {top: 40, right: 45, bottom: 30, left: 40}
      , width = 560// - margin.left - margin.right
      , height = 400// - margin.top - margin.bottom;
   var x = d3.scale.linear()
              .domain([0, d3.max(data, function(d) { return d[0]; })])
              .range([ 0, width ]);
   var y = d3.scale.linear()
    	      .domain([0, d3.max(data, function(d) { return d[1]; })])
    	      .range([ height, 0 ]);
   var chart = d3.select('body')
	.append('svg:svg')
	.attr('width', width + margin.right + margin.left)
	.attr('height', height + margin.top + margin.bottom)
	.attr('class', 'chart')
    var main = chart.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
	.attr('width', width)
	.attr('height', height)
	.attr('class', 'main')
    // draw the x axis
    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom');
    main.append('g')
	.attr('transform', 'translate(0,' + height + ')')
	.attr('class', 'main axis date')
	.call(xAxis);
	 chart.append("text")
        .attr("transform", "translate(" + (width) + " ," + (height + margin.bottom+40) + ")")
        .style("text-anchor", "middle")
        .text(xtitle);
    // draw the y axis
    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');
    main.append('g')
	.attr('transform', 'translate(0,0)')
	.attr('class', 'main axis date')
	.call(yAxis);
	chart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y",  margin.left-45)
        .attr("x",0 - (height / 2))
        .attr("dy", "5em")
        .style("text-anchor", "middle")
        .text(ytitle);
    var g = main.append("svg:g");
    g.selectAll("scatter-dot")
      .data(data)
      .enter().append("svg:circle")
          .attr("cx", function (d,i) { return x(d[0]); } )
          .attr("cy", function (d) { return y(d[1]); } )
          .attr("r", 2);
    g.append("text")
      .attr("class", "title")
      .attr("x", width/2)
      .attr("y", 0 - (margin.top / 2))
      .attr("text-anchor", "middle")
      .text(title);
   </script>
      </body>
    </html>
