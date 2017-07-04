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
    <title>Bar Chart</title>
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
    <div>
       <canvas id="bar-chart" width="80%" height="35%"></canvas>
    </div>

    <script>

      var data_labels = <?php echo $labels; ?>;
      var data_values = <?php echo $values; ?>;
      var data_xtitle = "<?php echo $xtitle; ?>"  ;
      var data_ytitle = "<?php echo $ytitle; ?>"  ;
      var data_title = "<?php echo $title; ?>"  ;


            new Chart(document.getElementById("bar-chart"),{
                type: 'bar',
                data: {
				              labels: data_labels,
                      datasets: [
                                  {
				                                label: data_ytitle,
                                        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95bd",
                                                          "#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95bd"],
                                        data: data_values
                                  }
                                ]
                      },
                options: {
                          scales: {
                              yAxes: [{
                                  scaleLabel: {
                                      display: true,
                                      labelString: data_ytitle
                                  }
                              }],
                              xAxes: [{
                                  scaleLabel: {
                                      display: true,
                                      labelString: data_xtitle
                                  }
                              }]
                          },
                    // Elements options apply to all of the options unless overridden in a dataset
                    // In this case, we are setting the border of each horizontal bar to be 2px wide
                    legend: {
                      display: false,
                    },
                    title: {
                        display: true,
                        text: data_title
                    }
                }
            });
        </script>
</body>

</html>
