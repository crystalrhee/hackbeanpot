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
		var isDisabled = $('#navAnalysis').is(':disabled');
		console.log(isDisabled);

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


// var isDisabled = $(element).is(':disabled');
//     if (isDisabled) {
//         $(element).prop('disabled', false);
//     } else {
//         // Handle input is not disabled
//     }