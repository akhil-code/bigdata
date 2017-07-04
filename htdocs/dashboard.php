
<?php
  ini_set('max_execution_time', 300);

  if ($_SERVER["REQUEST_METHOD"] == "POST") {

    if(strcmp($_POST["FILE_TYPE"],"TARGET")==0){

      $filename = "config\\dbDetails.txt";
      $myfile = fopen($filename,"w");
      fwrite($myfile,'ERROR_FLAG:0');
      fclose($myfile);

      $filename = "upload\\target_config.txt";
      $myfile = fopen($filename,"w");
      $hostName = test_input($_POST["hostname"]);
      $dbName = test_input($_POST["dbname"]);
      $username = test_input($_POST["username"]);
      $password = test_input($_POST["password"]);
      $tName = test_input($_POST["tname"]);
      $txt = "DETAILS_FLAG:1".PHP_EOL."hostname:".$hostName.PHP_EOL."dbname:".$dbName.PHP_EOL."username:".$username.PHP_EOL."password:".$password.PHP_EOL."tname:".$tName;
      fwrite($myfile,$txt);
      fclose($myfile);

      $filename = "upload\\target_config.txt";
      while(1){
        $temp_flag = 0;
        clearstatcache();
        if ( filesize($filename)>0 && (time() - filemtime($filename)) < 2){
          $lines = getLines($filename);
          foreach($lines as $line){
            if(strcmp($line,"DETAILS_FLAG:0") == 0){
              $temp_flag = 1;
            }
          }
        }

        if($temp_flag == 1){
          $filename = "config\\dbDetails.txt";
          $COL_FLAG = 0;

          $myfile = fopen($filename,"r");
          $temp_txt = fread($myfile,filesize($filename));
          fclose($myfile);

          $txt = $temp_txt.PHP_EOL."dbname:".$dbName.PHP_EOL."username:".$username.PHP_EOL."password:".$password.PHP_EOL."tname:".$tName.PHP_EOL."COL_FLAG:".$COL_FLAG.PHP_EOL."DETAILS_FLAG:1";
          $myfile = fopen($filename,"w");
          fwrite($myfile,$txt);
          fclose($myfile);


          while(1){
            $temp_flag = 0;
            clearstatcache();
            if ((time() - filemtime($filename)) < 2){
              $lines = getLines($filename);
              foreach($lines as $line){
                if(strcmp($line,"ERROR_FLAG:1") == 0){
                  // header("Location: \\dashboard.php");
                  echo '<script language="javascript">'
                  .'alert("Error:Please check your source details");'
                  .'</script>';
                  exit();

                }
                else if(strcmp($line,"ERROR_FLAG:2") == 0){
                  // header("Location: \\dashboard.php");
                  echo '<script language="javascript">'
                  .'alert("Error:Please check your target details");'
                  .'</script>';
                  exit();
                }
                else if(strcmp($line,"COL_FLAG:1") == 0){
                  $temp_flag = 1;
                }
              }
            }
            if($temp_flag == 1){
              header("Location: \\reports.php");
              exit();
              //break;

            }
            sleep(0.5);
          }
        }
        sleep(0.5);
      }

    }

    else if(strcmp($_POST["FILE_TYPE"],"MYSQL")==0 || strcmp($_POST["FILE_TYPE"],"MONGODB")==0){
      $filepath = "upload\\source_config.txt";
      $myfile = fopen($filepath,"w");

      $filetype = test_input($_POST["FILE_TYPE"]);

      $txt = "";
      $hostName = test_input($_POST["hostname"]);
      $txt = $txt."FILE_TYPE:".$filetype.PHP_EOL;
      $dbName = test_input($_POST["dbname"]);
      $username = test_input($_POST["username"]);
      $password = test_input($_POST["password"]);
      $tName = test_input($_POST["tname"]);
      $txt = $txt."hostname:".$hostName.PHP_EOL."dbname:".$dbName.PHP_EOL."username:".$username.PHP_EOL."password:".$password.PHP_EOL."tname:".$tName;
      if(strcmp($_POST["FILE_TYPE"],"MONGODB")==0){
        $port_no = test_input($_POST["port"]);
        $txt = $txt.PHP_EOL."port:".$port_no;
      }
      fwrite($myfile,$txt);
      fclose($myfile);
    }

    else if(strcmp($_POST["FILE_TYPE"],"CSV")==0 || strcmp($_POST["FILE_TYPE"],"JSON")==0 ||strcmp($_POST["FILE_TYPE"],"XML")==0){
      // Check if file was uploaded without errors
      if(isset($_FILES["myDoc"]) && $_FILES["myDoc"]["error"] == 0){
          $filename = $_FILES["myDoc"]["name"];
          $filetype = $_FILES["myDoc"]["type"];
          $filesize = $_FILES["myDoc"]["size"];

          // Verify file extension
          $ext = pathinfo($filename, PATHINFO_EXTENSION);
          //if(!array_key_exists($ext, $allowed)) die("Error: Please select a valid file format.");

          // Verify MYME type of the file
              // Check whether file exists before uploading it
              if(file_exists("upload/" . $_FILES["myDoc"]["name"])){

                $filepath = "upload\\source_config.txt";
                //$filename;
                $FILE_TYPE = test_input($_POST["FILE_TYPE"]);
                $myfile = fopen($filepath,"w");
                $txt = "FILE_TYPE:".$FILE_TYPE.PHP_EOL."FILE_NAME:".$filename;
                fwrite($myfile,$txt);
                fclose($myfile);

                echo '<script language="javascript">'
                // .'alert('.$_FILES["myDoc"]["name"].' already exists);'
                .'alert("file already exists ");'
                .'</script>';


              }
              else{

                $filepath = "upload\\source_config.txt";
                //$filename;
                $FILE_TYPE = test_input($_POST["FILE_TYPE"]);
                $myfile = fopen($filepath,"w");
                $txt = "FILE_TYPE:".$FILE_TYPE.PHP_EOL."FILE_NAME:".$filename;
                fwrite($myfile,$txt);
                fclose($myfile);

                echo '<script language="javascript">'
                .'alert("successfully uploaded file");'
                .'</script>';
                  move_uploaded_file($_FILES["myDoc"]["tmp_name"], "upload/" . $_FILES["myDoc"]["name"]);
                  // move_uploaded_file($_FILES["myDoc"]["tmp_name"], "C:\\spark\\bigDataAnalysis\\" . $_FILES["myDoc"]["name"]);




              }
      }

    }


  }


  function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }

  function getLines($filename){
    if(filesize($filename)<=0){
      return [''];
    }
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

    <style>
    .accordion-toggle h4:after {
    /* symbol for "opening" panels */
    font-family: 'Glyphicons Halflings';  /* essential for enabling glyphicon */
    content: "\e114";    /* adjust as needed, taken from bootstrap.css */
    float: right;        /* adjust as needed */
    color: white;         /* adjust as needed */
}
.accordion-toggle.collapsed h4:after {
    /* symbol for "collapsed" panels */
    content: "\e080";    /* adjust as needed, taken from bootstrap.css */
}

    </style>
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
                    <div class="panel panel-default">
                        <!-- <div class="panel-heading">

                        </div> -->
                        <!-- .panel-heading -->
                        <div class="panel-body">
                            <div class="panel-group" id="accordion">
                                <div class="panel panel-primary">
                                    <div class="panel-heading accordion-toggle"  data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
                                        <h4 class="panel-title">
                                            Provide source details
                                        </h4>

                                    </div>
                                    <div id="collapseOne" class="panel-collapse collapse in">
                                        <div class="panel-body">
                                          <div class="panel panel-info">
                                                <div class="panel-heading">
                                                    <!-- <i class="fa fa-bar-chart-o fa-fw"></i> -->
                                                     Source
                                                    <div class="pull-right">
                                                        <div class="btn-group">
                                                            <button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">
                                                                Select
                                                                <span class="caret"></span>
                                                            </button>
                                                            <ul class="dropdown-menu pull-right" role="menu">
                                                                <li><a onclick="showReqDiv('XML')">XML</a>
                                                                </li>
                                                                <li><a onclick="showReqDiv('CSV');">CSV</a>
                                                                </li>
                                                                <li><a onclick="showReqDiv('JSON');">JSON</a>
                                                                </li>
                                                                <li class="divider"></li>
                                                                <li><a onclick="showReqDiv('MySQL');">MySQL</a>
                                                                </li>
                                                                <li><a onclick="showReqDiv('Mongo');">Mongo</a>
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!-- /.panel-heading -->
                                                <div class="panel-body">
                                                    <div class="row">
                                                        <div class="col-md-4 col-md-offset-4">

                                                          <div id="dvForXML" style="display:none">
                                                            XML
                                                            <div class="form-group">
                                                              <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" enctype="multipart/form-data">
                                                              <label>File input</label>
                                                              <input type="file" name="myDoc" id="fileSelect">
                                                              <input type="submit" name="submit" value="Upload">
                                                              <input type="hidden" name="FILE_TYPE" value="XML">
                                                            </form>
                                                            </div>
                                                          </div>
                                                          <div id="dvForCSV" style="display:none">
                                                            CSV
                                                            <div class="form-group">
                                                              <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" enctype="multipart/form-data">
                                                              <label>File input</label>
                                                              <input type="file" name="myDoc" id="fileSelect">
                                                              <input type="submit" name="submit" value="Upload">
                                                              <input type="hidden" name="FILE_TYPE" value="CSV">
                                                            </form>
                                                            </div>
                                                          </div>

                                                          <div id="dvForJson" style="display:none">
                                                            Json
                                                            <div class="form-group">
                                                              <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" enctype="multipart/form-data">
                                                                <label>File input</label>
                                                                <input type="file" name="myDoc" id="fileSelect">
                                                                <input type="submit" name="submit" value="Upload">
                                                                <input type="hidden" name="FILE_TYPE" value="JSON">
                                                              </form>
                                                            </div>
                                                          </div>

                                                          <div id="dvForMySQL" style="display:none">
                                                            MySQL
                                                            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" role="form">
                                                                <div class="form-group">
                                                                <label>Host Name:</label>
                                                                <input type="text" name="hostname" class="form-control" placeholder="Enter Host Name" required autofocus>
                                                                </div>
                                                                <div class="form-group">
                                                                <label>Database  Name:</label>
                                                                <input type="text" name="dbname" class="form-control" placeholder="Enter Database  Name" required autofocus>
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Username:</label>
                                                                  <input type="text" name="username" class="form-control" placeholder="Enter Username" required>
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Password:</label>
                                                                  <input type="password" class="form-control" placeholder="Enter password" name="password" >
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Table name:</label>
                                                                  <input type="text" name="tname" class="form-control" placeholder="Enter table name" required>
                                                                </div>
                                                                  <input type="hidden" name="FILE_TYPE" value="MYSQL">
                                                                <br><br>
                                                                <button type="submit" value="submit" class="btn btn-success">Submit</button>
                                                            </form>
                                                          </div>

                                                          <div id="dvForMongo" style="display:none">
                                                            Mongo
                                                            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" role="form">
                                                                <div class="form-group">
                                                                <label>Host Name:</label>
                                                                <input type="text" name="hostname" class="form-control" placeholder="Enter Host Name" required autofocus>
                                                                </div>

                                                                <div class="form-group">
                                                                <label>Port:</label>
                                                                <input type="text" name="port" class="form-control" placeholder="Enter Port Number" required>
                                                                </div>

                                                                <div class="form-group">
                                                                <label>Database  Name:</label>
                                                                <input type="text" name="dbname" class="form-control" placeholder="Enter Database Name" required>
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Username:</label>
                                                                  <input type="text" name="username" class="form-control" placeholder="Enter Username" required>
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Password:</label>
                                                                  <input type="password" class="form-control" placeholder="Enter password" name="password">
                                                                </div>
                                                                <div class = "form_group">
                                                                  <label>Collection name:</label>
                                                                  <input type="text" name="tname" class="form-control" placeholder="Enter Collection name" required>
                                                                </div>
                                                                <input type="hidden" name="FILE_TYPE" value="MONGODB">

                                                                <br><br>
                                                                <button type="submit" value="submit" class="btn btn-success">Submit</button>
                                                            </form>
                                                          </div>

                                                        </div>
                                                    </div>
                                                    <!-- /.row -->
                                                </div>
                                                <!-- /.panel-body -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel panel-primary">
                                  <div class="panel-heading accordion-toggle"  data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">
                                      <h4 class="panel-title">
                                          Provide target details
                                      </h4>
                                  </div>
                                    <div id="collapseTwo" class="panel-collapse collapse">
                                        <div class="panel-body">
                                          <div class="panel panel-success">
                                              <div class="panel-heading">
                                                  Database details
                                              </div>
                                              <div class="panel-body">
                                                <div class="row">
                                                    <div class="col-md-4 col-md-offset-4">
                                                      <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post" role="form">
                                                          <div class="form-group">
                                                          <label>Host Name:</label>
                                                          <input type="text" name="hostname" class="form-control" placeholder="Enter Host Name" required autofocus>
                                                          </div>
                                                          <div class="form-group">
                                                          <label>Database  Name:</label>
                                                          <input type="text" name="dbname" class="form-control" placeholder="Enter Database  Name" required autofocus>
                                                          </div>
                                                          <div class = "form_group">
                                                            <label>Username:</label>
                                                            <input type="text" name="username" class="form-control" placeholder="Enter Username" required>
                                                          </div>
                                                          <div class = "form_group">
                                                            <label>Password:</label>
                                                            <input type="password" class="form-control" placeholder="Enter password" name="password">
                                                          </div>
                                                          <div class = "form_group">
                                                            <label>Table name:</label>
                                                            <input type="text" name="tname" class="form-control" placeholder="Enter table name" required>
                                                          </div>
                                                          <input type="hidden" name="FILE_TYPE" value="TARGET">

                                                          <br><br>
                                                          <button type="submit" value="submit" class="btn btn-success">Feed &amp; Analyze</button>
                                                      </form>
                                                    </div>
                                                </div>
                                              </div>

                                        </div>
                                    </div>
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

    function getFeedAnalysis()
    {
      //alert('feeded');
      window.location.href ="reports.html";
    }

    function showReqDiv(sourceType)
    {
        document.getElementById("dvForXML").style.display = "none";
        document.getElementById("dvForCSV").style.display = "none";
        document.getElementById("dvForJson").style.display = "none";
        document.getElementById("dvForMySQL").style.display = "none";
        document.getElementById("dvForMongo").style.display = "none";

      switch(sourceType) {
        case 'XML':
        //alert("good123456");
        document.getElementById("dvForXML").style.display = "block";
        break;
        case 'CSV':
          document.getElementById("dvForCSV").style.display = "block";
        break;
        case 'JSON':
          document.getElementById("dvForJson").style.display = "block";
        break;
        case 'MySQL':
        document.getElementById("dvForMySQL").style.display = "block";
        break;
        case 'Mongo':
          document.getElementById("dvForMongo").style.display = "block";
        break;
       //  default:
       //      code block
           }
    }



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
