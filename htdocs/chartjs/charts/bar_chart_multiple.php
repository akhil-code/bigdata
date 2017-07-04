<?php
  $filename = "..\\..\\config\\plotData.txt";
  $lines = getLines($filename);

  $data = array();
  for($x=2;$x<count($lines);$x++){
    $temp = explode(":",$lines[$x]);
    $data[$temp[0]] = $temp[1];
  }

  $xlabels = $data['xlabel'];
  $ylabel = $data['ylabel'];
  $yvalues1 = $data['yvalues1'];
  $yvalues2 = $data['yvalues2'];
  $legends = $data['legends'];
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

<!doctype html>
<html>

<head>
    <title>Bar Chart Multi Axis</title>
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
    <div style="width: 100%">
        <canvas id="myChart"></canvas>
    </div>
    <script>

    var xlabels = <?php echo $xlabels; ?>;
    var yvalues1 = <?php echo $yvalues1; ?>;
    var yvalues2 = <?php echo $yvalues2; ?>;
    var legends = <?php echo $legends; ?>;
    var xtitle = "<?php echo $xtitle; ?>" ;
    var ytitle = "<?php echo $ytitle; ?>" ;



  var ctx = document.getElementById("myChart").getContext("2d");

var data = {
    labels: xlabels,
    datasets: [
        {
            label: legends[0],
            backgroundColor: "blue",
            data: yvalues1
        },
        {
            label: legends[1],
            backgroundColor: "red",
            data: yvalues2
        }
    ]

};

var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        barValueSpacing: 20,
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
    </script>
</body>

</html>
