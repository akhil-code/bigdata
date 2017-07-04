<?php
  $filename = "..\\..\\config\\plotData.txt";
  $lines = getLines($filename);

  $data = array();
  for($x=2;$x<count($lines);$x++){
    $temp = explode(":",$lines[$x]);
    $data[$temp[0]] = $temp[1];
  }

  $labels = $data['labels'];
  $values = $data['values'];

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
    <title>Horizontal Bar Chart</title>
    <script src="../Chart.bundle.js"></script>
    <script src="../Chart.HorizontalBar.js"></script>
    <style>
    canvas {
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    </style>
</head>

<body>
    <div>
       <canvas id="canvas" width="80%" height="45%"></canvas>
    </div>

<script>

var data_labels = <?php echo $labels; ?>;
var data_values = <?php echo $values; ?>;

var ctx = document.getElementById("canvas").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: data_labels,
        datasets: [{
            label: '# of Votes',
            data: data_values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>
        </script>
</body>

</html>
