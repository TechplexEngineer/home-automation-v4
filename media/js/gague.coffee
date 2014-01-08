class App.Gague
	constructor: (@name, @id, options) ->
		@options = 
			min:		0
			max:		200
			greenFrom:	65
			greenTo:	100
			yellowFrom:	100
			yellowTo:	150
			redFrom:	150
			redTo:		200
			minorTicks:	5
			width:		250
			height:		250
		$.extend(@options, options)

		@data = google.visualization.arrayToDataTable([
			[@name],
			[0]
		])
		if $(@id).length == 0
			$('body').append('<div id="'+@id+'"></div>')
		

		@gague = new google.visualization.Gauge(document.getElementById(@id));
		@gague.draw(@data, @options)

	update: (newdata) ->
		@data.setValue(0, 0, newdata);
		@gague.draw(@data, @options);
	
