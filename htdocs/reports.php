<?php

  ini_set('max_execution_time', 300);


  $GRAPH_TYPES = array('Bar chart','Piechart','Histogram','Scatter plot','Bar chart multiple',
                 'Bar chart horizontal','Bar chart versus','Line chart');
  ini_set('max_execution_time', 300);

  function areSame($arr1,$arr2){
    $temp = array_merge(array_diff($arr1,$arr2),array_diff($arr2,$arr1));
    return count($temp) == 0?true:false;
  }

  $col_data = array();
  $sugg_tables = array();

  if(!isset($PLOT_PATH))
  $PLOT_PATH = '';

  $filename = "config\\cols.txt";
  $myfile = fopen($filename,"r");
  $txt = fread($myfile,filesize($filename));
  $lines = explode(PHP_EOL,$txt);
  foreach($lines as $line){
    if(strcmp($line,"")==0){
      continue;
    }
    $temp = explode(":",$line);
    $col_data[$temp[0]] = $temp[1];
  }

  $choices = array();

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if(strcmp($_POST['REQUESTTYPE'],'SUGGEST')==0){
      $OPTIONS = ["int","discrete","boolean","string","double","timestamp"];
      $choices = $_POST;
      unset($choices['REQUESTTYPE']);
      $keys = array_keys($choices);
      $values = array_values($choices);//data types
      switch(count($choices)){
        case 1:
          $ch_type = $choices[$keys[0]];
          #int or double: pie chart,bar chart,histogram
          if(strcmp($ch_type,$OPTIONS[0]) == 0 || strcmp($ch_type,$OPTIONS[4])==0){
            array_push($sugg_tables,$GRAPH_TYPES[0],$GRAPH_TYPES[1],$GRAPH_TYPES[2]);
          }
          #discrete: pie chart,bar chart
          else if(strcmp($ch_type,$OPTIONS[1])==0){
            array_push($sugg_tables,$GRAPH_TYPES[0],$GRAPH_TYPES[1]);

          }
          else if(strcmp($ch_type,$OPTIONS[2])==0){
            array_push($sugg_tables,$GRAPH_TYPES[0],$GRAPH_TYPES[1]);
          }
          break;
        case 2:
          $ch_req = [[$OPTIONS[0],$OPTIONS[0]],[$OPTIONS[0],$OPTIONS[4]],
                    [$OPTIONS[0],$OPTIONS[2]],[$OPTIONS[4],$OPTIONS[2]],[$OPTIONS[1],$OPTIONS[2]],
                    [$OPTIONS[0],$OPTIONS[5]],[$OPTIONS[2],$OPTIONS[5]],[$OPTIONS[4],$OPTIONS[5]]];

          #int,int:scatter plots
          #double,int:scatter plots
          if (areSame($values,$ch_req[0]) || areSame($values,$ch_req[1])){
            array_push($sugg_tables,$GRAPH_TYPES[3]);
          }
          #int,bool or dis,bool or double,bool: bar chart
          else if (areSame($values,$ch_req[2]) || areSame($values,$ch_req[3])|| areSame($values,$ch_req[4])){
            array_push($sugg_tables,$GRAPH_TYPES[6]);
          }
          #int,date or bool,date: line chart
          else if (areSame($values,$ch_req[5]) || areSame($values,$ch_req[6]) || areSame($values,$ch_req[7])){
            array_push($sugg_tables,$GRAPH_TYPES[7]);
            }
          break;
        case 3:
          #ch_req[0]:discrete,boolean,boolean
          #ch_req[1]:int,boolean,boolean
          #ch_req[2]:double,boolean,boolean
          $ch_req = [[$OPTIONS[1],$OPTIONS[2],$OPTIONS[2]],[$OPTIONS[0],$OPTIONS[2],
                      $OPTIONS[2]],[$OPTIONS[4],$OPTIONS[2],$OPTIONS[2]]];
          #discrete,boolean,boolean:bar chart multiple
          if(areSame($values,$ch_req[0])){
            array_push($sugg_tables,$GRAPH_TYPES[4]);
          }
          #int,boolean,boolean:bar chart multiple
          #double,boolean,boolean:bar chart multiple
          else if(areSame($values,$ch_req[1]) || areSame($values,$ch_req[2])){
            array_push($sugg_tables,$GRAPH_TYPES[4]);
          }
          break;
        default:
          1+1;
        break;
      }//switch

    }//innerif

    else{

      $keys = array_keys($_POST);
      $values = array_values($_POST);

      $graphName = $keys[0];
      $selections = $values[0];
      $selections = json_decode($selections,true);

      $keys = array_keys($selections);
      $values = array_values($selections);


      $myfile = fopen("config\\selection.txt","w");
      $txt = "REQUEST_FLAG:1".PHP_EOL."RESPONSE_FLAG:0".PHP_EOL;
      $txt = $txt."GraphName:".$graphName.PHP_EOL;
      for($i=0;$i<count($keys);$i++){
        $txt = $txt.$keys[$i].":".$values[$i].PHP_EOL;
      }
      fwrite($myfile,$txt);
      fclose($myfile);

      $filename = "config\\plotData.txt";
      $temp_flag = 0;

      while(1){
        clearstatcache();
        if ((time() - filemtime($filename)) < 2){
          if(filesize($filename)>0){
            $lines = getFlags($filename);
          }

          else{
            continue;
          }

          foreach($lines as $line){
            if(strcmp($line,"RESPONSE_FLAG:1") == 0){
              $temp_flag = 1;
            }
          }
        }
        if($temp_flag == 1){
          // echo 'looping out';
          $graph = explode(":",$lines[1]);
          // echo $graph[1];


          if($graph[1] ==$GRAPH_TYPES[0]){
            $PLOT_PATH = "\\chartjs\\charts\\bar_chart.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[1]){
            $PLOT_PATH =  "\\chartjs\\charts\\pie_chart.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[2]){
            $PLOT_PATH = "\\chartjs\\charts\\histogram.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[3]){
            $PLOT_PATH = "\\chartjs\\charts\\scatter.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[4]){
            $PLOT_PATH = "\\chartjs\\charts\\bar_chart_multiple.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[5]){
            $PLOT_PATH = "\\chartjs\\charts\\hBar_chart.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[6]){
            $PLOT_PATH = "\\chartjs\\charts\\bar_chart.php";
          }
          else if($graph[1] ==$GRAPH_TYPES[7]){
            $PLOT_PATH = "\\chartjs\\charts\\line_chart.php";
          }

          // $_GLOBAL['value'] = $PLOT_PATH;
          break;
        }
        sleep(0.5);
      }//while loop


      }
  }


  function getFlags($filename){
    $myfile = fopen($filename,"r");
    $txt = fread($myfile,filesize($filename));
    $lines = explode(PHP_EOL,$txt);
    fclose($myfile);
    return $lines;
  }


?>

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Data Feed - Start Feeding</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/stylish-portfolio.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css">


</head>

  <body style="background: url(img/1.jpg); background-size:cover">
  <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html" style="color: #fff !important">Data Feeding &amp; Analytics</a>
            </div>

        </div>
        <!-- /.container -->
    </nav>



    <div class="container-fluid" style="margin-top:40px; ">

            <div class="row">
                <div class="col-lg-12 text-center">
                    <h1></h1>
                    <div class="panel panel-info">
                        <div class="panel-heading">
                            Reports for your business
                        </div>
                        <!-- .panel-heading -->
                        <div class="panel-body">
                          <div class="row">
                                <div class="col-md-2" style="border-right:1px dotted #CFCFCF">
                                  <h4>Data fields</h4>
                                  <div id="cols_tab" style="margin-left:30px;" align="left"></div>
                                  <div id="sugg_tab" style="margin-left:30px;" align="left"></div>

                                </div>
                                <!-- /.col-lg-4 (nested) -->
                                <div class="col-md-10">
                                         <h4>Chart</h4>
                                         <iframe id="chart_tab" scrolling="no" height="500" width="800" style="border:none;" ></iframe>
                                </div>
                            </div>
                          </div>
                        <!-- .panel-body -->
                    </div>
                </div>
            </div>
            <!-- /.row -->

    </div>


    <footer>
        <div class="container">
            <div class="row">
                <div class="col-md-10 col-md-offset-1 text-center">

                </div>
            </div>
        </div>
        <a id="to-top" href="#top" class="btn btn-dark btn-lg"><i class="fa fa-chevron-up fa-fw fa-1x"></i></a>
    </footer>

    <!-- jQuery -->
    <script src="js/jquery-3.2.1.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- Custom Theme JavaScript -->
    <script>
    var col_data = <?php echo json_encode($col_data); ?>;

    var col_doc = "";
    var ind = 0;
    var form = '<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post">';
    col_doc += form+""
    for (var key in col_data){
      var ch_box = '<div class="checkbox"><label><input type="checkbox" id='+ind+' name="'+key+'" value='+col_data[key]+'>'+key+'</label></div>';
      ind += 1;
      col_doc += ch_box;
    }
    col_doc += '<input type="hidden" name="REQUESTTYPE" value="SUGGEST">'
    col_doc += '<input type="submit" value="fetch Graphs"></form><br>';
    document.getElementById("cols_tab").innerHTML = col_doc;


    var sugg_data = <?php echo json_encode($sugg_tables); ?>;
    var choices = <?php echo json_encode($choices); ?>;

    var y = '';
    for(x in sugg_data){
      y += sugg_data[x];
    }
    choices = JSON.stringify(choices);

    if(sugg_data.length != 0){
      var sugg_doc = '<h4>Suggested Graphs</h4>';
      sugg_doc += '<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post">';
      // sugg_doc += '<form action="plot.php" method="post">';

      for(x in sugg_data){
        var rad_box = '<input type="radio" name="'+sugg_data[x]+'" value=\''+choices+'\'>'+sugg_data[x]+'<br>';
        sugg_doc += rad_box;
      }
      sugg_doc += '<input type="hidden" name="REQUESTTYPE" value="PLOT">'
      sugg_doc += '<br><input type="submit" value="Plot">';
      sugg_doc += '</form>';
      document.getElementById("sugg_tab").innerHTML = sugg_doc;
    }

    var plot_path = (<?php echo json_encode($PLOT_PATH); ?>);
    document.getElementById('chart_tab').src = plot_path;


    var fixed = false;
    $(document).scroll(function() {
        if ($(this).scrollTop() > 250) {
            if (!fixed) {
                fixed = true;
                // $('#to-top').css({position:'fixed', display:'block'});
                $('#to-top').show("slow", function() {
                    $('#to-top').css({
                        position: 'fixed',
                        display: 'block'
                    });
                });
            }
        } else {
            if (fixed) {
                fixed = false;
                $('#to-top').hide("slow", function() {
                    $('#to-top').css({
                        display: 'none'
                    });
                });
            }
        }
    });

    </script>

</body>

</html>
