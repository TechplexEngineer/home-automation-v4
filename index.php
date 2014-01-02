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
		<script src="jquery-1.10.2.min.js" type="text/javascript"></script>
	</head>
	<body>
		<h1>Home Heating Control</h1>
		<?php
		echo $twig->render('template.html', array("data"=>$zones));
		?>
		
	</body>
</html>


