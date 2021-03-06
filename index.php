<?php

#print_r($_SERVER);

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
			if ($row['finished'] != 1)
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
		<script type="text/javascript" src="media/js/jquery-2.0.3.min.js"></script>
		<script type="text/javascript" src="media/js/moment.min.js"></script>
		<script type="text/javascript">
			$(document).ready(function(){

				//using window.performance.now() I found hthat this function can take 1000-200ms
				function refreshStatus()
				{
					var url = "/cgi-bin/api.py?action=read&fmt=raw"
					$.get(url, function(data) {
						for (var i=0; i<6; i++)
						{
							if (data & 1<<i)
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('off').addClass('on').attr('title','On');
							else
								$('tr.zone_'+i+' td.zone_status .circle').removeClass('on').addClass('off').attr('title','Off');
						}
					}).always(function(){
						refreshStatus();
					});
				}
				//as soon as the page is ready, go!
				refreshStatus();
				// setInterval(refreshStatus, 5*1000);

				//when the user clicks a radio button make the api call to cause action
				$('input[type="radio"]').on('click', function(){
					var zone = $(this).attr('name').match(/zone\[(\d)\]/)[1];
					var action = $(this).val();
					var duration = $('[name="duration"]').val();

					duration = parseFloat(duration);
					if (isNaN(duration)) {
						alert('Invalid duration. Must be a number.');
						return;
					}
					console.log("Set zone %s to state %s", zone, action);
					var url = "/cgi-bin/api.py?action="+action+"&zone="+zone+"&duration="+duration

					$.get(url, function(data) {

						if (action != "thermostat")
						{
							data = data.replace(/(\n|\r)+$/, '')
							var date = moment(data+' UTC');

							//in theory the response data should be 1 on success
							$('tr.zone_'+zone+' td.until')
								.html(date.format("h:mm a MM/DD/YY"))
								.data('exp', date);
						}
						else {
							$('tr.zone_'+zone+' td.until').html("--");
						}
						console.log("Action Comitted!");
					});
				});

				//clear completed intervals
				setInterval(function(){
					$('tr.zone td.until').each(function(idx, el){
						var val = $(el).data('exp');
						if(val && moment().isAfter(moment(val))) {
							$(el).data('exp','').html('--');
							var zone = $(el).parent().find('td:first-child').html().trim();
							$('[name="zone['+zone+']"][value="thermostat"]').prop('checked',true);
						}
					});
				}, 60*1000);
			});
		</script>
		<script type="text/javascript" src="media/js/svg.min.js"></script>
		<!-- <script type="text/javascript" src="media/js/jsapi.js"></script> -->
		<script type="text/javascript">
			// google.load('visualization', '1', {packages: ['gauge']})
			App = { };
		</script>
		<script type="text/javascript" src="media/js/coffee-script.js"></script>
		<script type="text/coffeescript" src="media/js/tank.coffee"></script>
		<!-- <script type="text/coffeescript" src="media/js/gague.coffee"></script> -->
		<script type="text/javascript">
			$(document).ready(function(){

				var handle = setInterval(function(){
					if (App && App.Tank)
					{
						clearInterval(handle);
						init();
					}
					// if the tank code isn't ready yet, try again in half a second or so
				},500);
			});
			function init()
			{
				// var internalGague = new App.Gague('Internal','intgague');
				var tankSVG = new App.Tank('tank');

				function loadTempData() {
					url = "/cgi-bin/api.py?action=temp"
					$.get(url, function (data) {
						// internalGague.update(data.internal);
						$('#intgague').text("Furnace room: " + data.internal + "\xB0F")
						tankSVG.update(data.tank_top,data.tank_mid,data.tank_bot);
					});
				}
				loadTempData();

				// update the temp data every 5 seconds
				setInterval(loadTempData, 5*1000);
			}
		</script>
	</head>
	<body>
		<h1>Home Heating Control</h1>
		<div class="form-group">
			<label class="control-label" for="duration">Duration (Hour)</label>
			<input name="duration" type="text" value="1" class="form-control"/>
		</div>
		<?php
		echo $twig->render('template.html', array("data"=>$zones));
		?>
		<h1>Status</h1>
		<div id="tank" class="inline-block"></div>
		<div id="intgague"></div>
	</body>
</html>


