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
  $title = $data['title'];
  $xtitle = $data['xtitle'];

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
    <title>Pie Chart</title>
    <script src="../Chart.bundle.js"></script>
    <script src="../utils.js"></script>
</head>

<body>
    <div id="canvas-holder" style="width:50%" align="center">
        <canvas id="chart-area" />
    </div>
    <script>

    var data_labels = <?php echo $labels; ?>;
    var data_values = <?php echo $values; ?>;
    var data_title = "<?php echo $title; ?>";
    var data_xtitle = "<?php echo $xtitle; ?>";




    var config = {
        type: 'pie',
        data: {
            datasets: [{
                data: data_values,
                backgroundColor: [
                    window.chartColors.red,
                    window.chartColors.orange,
                    window.chartColors.yellow,
                    window.chartColors.green,
                    window.chartColors.blue,
                    window.chartColors.red,
                    window.chartColors.orange,
                    window.chartColors.yellow,
                    window.chartColors.green,
                    window.chartColors.blue
                ],
              //  label: 'Dataset 1'
            }],
            labels: data_labels
        },
        options: {
            responsive: true,
			title: {
                        display: true,
                        text: data_title
                    },
					 legend: {
                      display: true,
                    }
        }
    };

    window.onload = function() {
        var ctx = document.getElementById("chart-area").getContext("2d");
        window.myPie = new Chart(ctx, config);
    };

    </script>
</body>

</html>
