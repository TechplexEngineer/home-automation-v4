<?php

require_once 'Twig/Autoloader.php';
Twig_Autoloader::register();

$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader
/*	, array(
    'cache' => 'templates/compilation_cache',
)*/);

$db = new SQLite3('/var/www/db/log.db');

$zones = array(
	array( "title"=>"Master Bed Room", 		"num"=>3, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" ),
	array( "title"=>"Blake's Bed Room", 	"num"=>2, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" ),
	array( "title"=>"First Floor", 			"num"=>4, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" ),
	array( "title"=>"First Floor Radiant", 	"num"=>1, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" ),
	array( "title"=>"Domestic Hot Water", 	"num"=>5, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" ),
	array( "title"=>"Basement Radiant", 	"num"=>0, "status"=>-1, "ctrl"=>"thermostat", "until"=>"--" )
);

$results = $db->query('SELECT * FROM last_zone_action ORDER BY zone');
while ($row = $results->fetchArray()) {
	foreach ($zones as $idx => $zone) {
		if ($zone["num"] == $row['zone'])
		{
			$zones[$idx]["ctrl"] = $row['action'];
			// print $zone["num"] . " | " . $row['action'] . " | " . $row['expiration'] . "\n";
			if (strcasecmp($row['action'],"thermostat") != 0)
			{
				//convert utc time to "localtime"
				$time = strtotime($row['expiration'].' UTC');
				$dateInLocal = date("g:i a m/d/y", $time);

				$zones[$idx]["until"] = $dateInLocal;
			}
		}

		// print $idx ." ". $row['action']."\n";

		// if (strcasecmp($row['action'],"thermostat") != 0)
		// 	$zones[$idx]["until"] = $row['expiration'];
	}
}
?>


<html>
	<head>
		<title>Heating Control Panel</title>
		<link rel="stylesheet" href="media/css/style.css">
		<script src="media/js/jquery-2.0.3.min.js" type="text/javascript"></script>
		<script type="text/javascript">
			$(document).ready(function(){

				//using window.performance.now() I found hthat this function can take 1000-200ms
				function refreshStatus()
				{
					var url = "http://home-automation/cgi-bin/api.py?action=read&fmt=raw"
					$.get(url, function(data) {
						for (var i=0; i<6; i++)
						{
							if (data & 1<<i)
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('off').addClass('on').attr('title','On');
							else
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('on').addClass('off').attr('title','Off');
						}
					});
				}
				//as soon as the page is ready, go!
				refreshStatus();
				setInterval(refreshStatus, 2*1000);

				//when the user clicks a radio button make the api call to cause action
				$('input[type="radio"]').on('click', function(){
					// console.log("Click Detected");
					var zone = $(this).attr('name').match(/zone\[(\d)\]/)[1];
					var action = $(this).val();
					console.log("Set zone %s to state %s", zone, action);
					var url = "http://home-automation/cgi-bin/api.py?action="+action+"&zone="+zone
					// console.log("Requesting: ", url);

					$.get(url, function(data) {
						data = data.replace(/(\n|\r)+$/, '')
						console.log("Response: ",data); //chomp the newline
						//in theory the response data should be 1 on success
						$('tr.zone_'+zone+' td.until').html(data);
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


