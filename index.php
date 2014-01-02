<?php

require_once 'Twig/Autoloader.php';
Twig_Autoloader::register();

$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader
/*	, array(
    'cache' => 'templates/compilation_cache',
)*/);

$zones = array(
array( "title"=>"Master Bed Room", 		"num"=>0, "status"=>-1 ),
array( "title"=>"Blake's Bed Room", 	"num"=>1, "status"=>-1 ),
array( "title"=>"First Floor", 			"num"=>2, "status"=>-1 ),
array( "title"=>"First Floor Radiant", 	"num"=>3, "status"=>-1 ),
array( "title"=>"Domestic Hot Water", 	"num"=>4, "status"=>-1 ),
array( "title"=>"Basement Radiant", 	"num"=>5, "status"=>-1 )
);

?>


<html>
	<head>
		<title>Heating Control Panel</title>
		<link rel="stylesheet" href="style.css">
		<script src="jquery-2.0.3.min.js" type="text/javascript"></script>
		<script type="text/javascript">
			$(document).ready(function(){

				setInterval(function(){
					var url = "http://home-automation/cgi-bin/api.py?action=read&fmt=raw"
					$.get(url, function(data) {
						for (var i=0; i<6; i++)
						{
							if (data & 1<<i)
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('off').addClass('on').attr('title','On');
							else
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('on').addClass('off').attr('title','Off')
						}
					});
				}, 2*1000);
	/*
				var socket = io.connect(window.location.hostname);
				socket.on('statusEvt', function (data) {
					
					//- console.log(data); 
					//update the status circles
				});
	*/
				$('input[type="radio"]').on('click', function(){
					console.log("Click Detected");
					var zone = $(this).attr('name').match(/zone\[(\d)\]/)[1];
					var action = $(this).val();
					console.log(zone, action);
					var url = "http://home-automation/cgi-bin/api.py?action="+action+"&zone="+zone
					console.log("Requesting: ", url);

					$.get(url, function(data) {
						console.log("Response: ",data)
						//$(".result").html( data );
						//alert( "Load was performed." );
					});
				});
			});

		</script>
	</head>
	<body>
		<h1>Home Heating Control</h1>
		<?php
		echo $twig->render('template.html', array("data"=>$zones));
		?>
		
	</body>
</html>


