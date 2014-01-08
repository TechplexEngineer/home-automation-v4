google.load('visualization', '1', {packages: ['gauge']});


// var gauge;
// var gaugeData;
// var gaugeOptions;
// function drawGaugeold() {
// 	gaugeData = google.visualization.arrayToDataTable([
// 		['Internal'],
// 		[0] //default values
// 	]);

// 	gauge = new google.visualization.Gauge(document.getElementById('gauge'));
// 	gaugeOptions = {
// 			min: 0,
// 			max: 200,
// 			greenFrom: 65,
// 			greenTo: 100,
// 			yellowFrom: 100,
// 			yellowTo: 150,
// 			redFrom: 150,
// 			redTo: 200,
// 			minorTicks: 5,
// 			width:250,
// 			height:250
// 	};
// 	gauge.draw(gaugeData, gaugeOptions);
// }


var internal = {
	name: 'Internal',
	id: 'intgague',
	options: {
		min: 0,
		max: 200,
		greenFrom: 65,
		greenTo: 100,
		yellowFrom: 100,
		yellowTo: 150,
		redFrom: 150,
		redTo: 200,
		minorTicks: 5,
		width:250,
		height:250
	}
};

function drawGague(opt) {
	opt['data'] = google.visualization.arrayToDataTable([
		[opt['name']],
		[0] //default values
	]);
	opt['gague'] = new google.visualization.Gauge(document.getElementById(opt['id']));
	opt['gague'].draw(opt['data'], opt['options']);
	return opt['gague']
}
// --------------------------------------------------------------
function init() {
	drawGague(internal);
}

google.setOnLoadCallback(init);
// --------------------------------------------------------------
function loadTempData()
{
	var url = "http://home-automation/cgi-bin/api.py?action=temp"
	$.get(url, function(data) {

		internal['data'].setValue(0, 0, data.internal);
		internal['gague'].draw(internal['data'], internal['options']);
	});
}
setInterval(loadTempData, 2*1000)
