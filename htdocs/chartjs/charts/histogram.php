<?php
  $filename = "..\\..\\config\\plotData.txt";
  $lines = getLines($filename);

  $data = array();
  for($x=2;$x<count($lines);$x++){
    $temp = explode(":",$lines[$x]);
    $data[$temp[0]] = $temp[1];
  }

  $xvalues = $data['xvalues'];
  $xtitle = $data['xtitle'];
  $title = $data['title'];

  function getLines($filename){
    $myfile = fopen($filename,"r");
    $txt = fread($myfile,filesize($filename));
    $lines = explode(PHP_EOL,$txt);
    fclose($myfile);
    return $lines;
  }
?>

	<html>
		<head>
		<!-- Plotly.js -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
        <!-- Plotly chart will be drawn inside this DIV -->
        <div id="myDiv"></div>
        <script>
        var x = <?php echo $xvalues; ?>;
        var xtitle = "<?php echo $xtitle; ?>";
        var title = "<?php echo $title; ?>";


		var data = [
			{
				x: x,
				type: 'histogram',
				marker: {
					color: 'rgba(0,0,250,0.7)',
				},
			}
		];

    layout = {                     // all "layout" attributes: #layout
    title: title,  // more about "layout.title": #layout-title
    xaxis: {                  // all "layout.xaxis" attributes: #layout-xaxis
        title: xtitle         // more about "layout.xaxis.title": #layout-xaxis-title
    },
    annotations: [            // all "annotation" attributes: #layout-annotations
        {
            text: 'frequency',    // #layout-annotations-text
            x: 0,                         // #layout-annotations-x
            xref: 'paper',                // #layout-annotations-xref
            y: 0,                         // #layout-annotations-y
            yref: 'paper'                 // #layout-annotations-yref
        }
    ]
    }
		Plotly.newPlot('myDiv', data,layout);
        </script>
        </body>
	</html>
