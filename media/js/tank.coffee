class App.Tank
	constructor: (where, options) ->
		@options = 
			toptemp:	'?'
			midtemp:	'?'
			bottemp:	'?'
			colorRed:	'red'
			width:		100
			tankcolor:	'#472E26'
			elheight:	50
			tankheight:	180

			# min:		0
			# max:		200
			# greenFrom:	65
			# greenTo:	100
			# yellowFrom:	100
			# yellowTo:	150
			# redFrom:	150
			# redTo:		200
			# minorTicks:	5
			# width:		250
			# height:		250
		$.extend(@options, options)

		@draw = SVG(where).size(@options.width+10, @options.tankheight+@options.elheight+10)

		# tank body
		@draw
			.rect(@options.width,@options.tankheight)
			.move(0,@options.elheight/2)
			.fill(@options.tankcolor)
		# tank top
		@draw
			.ellipse(@options.width,@options.elheight)
			.fill(@options.tankcolor)
		# tank bottom
		@draw
			.ellipse(@options.width,@options.elheight)
			.move(0,@options.tankheight)
			.fill(@options.tankcolor)
		# draw legs (left, right)
		@draw
			.rect(4,20)
			.move(15,@options.tankheight+35)
		@draw
			.rect(4,20)
			.move(100-(15+4),@options.tankheight+35)

		@topTemp = @draw
			.text(@options.toptemp+'\xB0F')
			.center(@options.width/2,@options.elheight/2)
			.fill(@options.colorRed)
		@midTemp = @draw
			.text(@options.midtemp+'\xB0F')
			.center(@options.width/2,@options.tankheight/2+@options.elheight/2-5)
			.fill(@options.colorRed)
		@botTemp = @draw
			.text(@options.bottemp+'\xB0F')
			.center(@options.width/2,@options.tankheight+@options.elheight/2-15)
			.fill(@options.colorRed)

	update: (top, mid, bot) ->
		@topTemp
			.text(top+'\xB0F')
			.center(@options.width/2,@options.elheight/2)
			.fill(@options.colorRed)
		@midTemp
			.text(mid+'\xB0F')
			.center(@options.width/2,@options.tankheight/2+@options.elheight/2)
			.fill(@options.colorRed)
		@botTemp
			.text(bot+'\xB0F')
			.center(@options.width/2,@options.tankheight+@options.elheight/2-15)
			.fill(@options.colorRed)


# tankSVG = new Tank('tank');

# loadTempData = () -> 
# 	url = "http://home-automation/cgi-bin/api.py?action=temp"
# 	$.get(url,  (data) ->
# 		# console.log data
# 		tankSVG.update(data.tank_top,data.tank_mid,data.tank_bot)
# 	)


# setInterval(loadTempData, 2*1000)

