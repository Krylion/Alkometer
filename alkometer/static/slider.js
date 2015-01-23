$("document").ready(
	function()
	{	
		rotateImgs();
	}
);

function rotateImgs()
{
	var firstImg = $(".imgToRotate:first-child");
	var title = $(".imgToRotate:first-child title");
	firstImg.addClass("current");
	
	rotate();
}

function rotate()
{

	var current = $(".current");
	
	current.animate(
	{
		"opacity": 0
	}, 5200, function()
	{
		$(this).removeClass("current");
	}
	);	
	
	current = current.next();
	 if (current[0] ==  undefined)
	   current = $(".imgToRotate:first-child");
	   
	current.css("opacity", 0).addClass("current").delay(200).animate({"opacity": 1.0}, 5800, rotate);
}
