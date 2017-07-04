<?php
  $filename = "..\\..\\config\\plotData.txt";
  $lines = getLines($filename);

  $data = array();
  for($x=2;$x<count($lines);$x++){
    $temp = explode(":",$lines[$x]);
    $data[$temp[0]] = $temp[1];
  }

  $xvalues = $data['xvalues'];
  $yvalues = $data['yvalues'];
  $xtitle = $data['xtitle'];
  $ytitle = $data['ytitle'];
  $title = $data['title'];


  function getLines($filename){
    $myfile = fopen($filename,"r");
    $txt = fread($myfile,filesize($filename));
    $lines = explode(PHP_EOL,$txt);
    fclose($myfile);
    return $lines;
  }
?>

<!doctype html>
<html>

<head>
    <title>Scatter Chart</title>
    <script src="../Chart.bundle.js"></script>
    <script src="../utils.js"></script>
    <style>
    canvas {
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    </style>
</head>

<body>
    <div style="width:75%">
        <canvas id="myChart"></canvas>
    </div>
    <script>
    var xvalues = <?php echo $xvalues; ?>;
    var yvalues = <?php echo $yvalues; ?>;
    var xtitle = "<?php echo $xtitle; ?>";
    var ytitle = "<?php echo $ytitle; ?>";
    var title = "<?php echo $title; ?>";


  var my_data = [];
  var i=0;
  for(i=0;i<xvalues.length;i++){
    my_data.push(getDict(xvalues[i],yvalues[i]));
  }



	var color = Chart.helpers.color;
	var scatterChartData = {
        datasets: [{
            label: ytitle,
			borderColor: window.chartColors.red,
            backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
            data:my_data,
        }] // datasets
    }; //chartData

    window.onload = function() {
            var ctx = document.getElementById("myChart").getContext("2d");
            window.myScatter = Chart.Scatter(ctx, {
                data: scatterChartData,
                options: {
                    title: {
                        display: true,
                        text: title
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                            }
                        },
                        {
                            scaleLabel: {
                                display: true,
                                labelString: ytitle
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: xtitle
                            }
                        }]
                    }
                }
            });
        };

    function getDict(a,b){
      return {'x':a,'y':b}
    }
    </script>
</body>
