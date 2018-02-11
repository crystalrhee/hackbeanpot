$(window).on("load",function(){
	$(".loader").fadeOut("slow");;
});

$(function() {
	$('.text-input textarea').prop('required',true);
});

$(function() {
	$('.input.submit input').click(function() {
		e.preventDefault();
		$location.hash() = '#analysis'
	});
});

$(function() {
	$('#navAnalysis').click(function() {
		pro = $('#resultPro')[0].innerHTML;
		con = $('#resultCon')[0].innerHTML;
		console.log(pro);
		console.log(con);
		proPercent = (pro * 100).toFixed(2) + '%';
		conPercent = (con * 100).toFixed(2) + '%';
		$('#bar-1').css('width', proPercent);
		$('#bar-1').html(proPercent);
		$('#bar-2').css('width', conPercent);
		$('#bar-2').html(conPercent);
	});
});