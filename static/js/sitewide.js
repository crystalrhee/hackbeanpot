$(window).on("load",function(){
	$(".loader").fadeOut("slow");;
	$('.text-input textarea').attr('placeholder','Select a category and add text here to analyze.');
});

$(function() {
	$('.text-input textarea').prop('required',true);
});

$(function() {
	$('#navAnalysis').click(function() {
		pro = $('#resultPro')[0].innerHTML;
		con = $('#resultCon')[0].innerHTML;
		proPercent = (pro * 100).toFixed(2) + '%';
		conPercent = (con * 100).toFixed(2) + '%';
		$('#bar-1').css('width', proPercent);
		$('#bar-1').html(proPercent);
		$('#bar-2').css('width', conPercent);
		$('#bar-2').html(conPercent);
	});
});

$(function() {
	$('#labels ul :nth-child(1)').hover(function() {
		$('#bar-1').toggleClass("filter");
	});
	$('#labels ul :nth-child(2)').hover(function() {
		$('#bar-2').toggleClass("filter");
	});
	$('#bar-1').hover(function() {
		$(this).toggleClass("filter");
	});
	$('#bar-2').hover(function() {
		$(this).toggleClass("filter");
	});
});