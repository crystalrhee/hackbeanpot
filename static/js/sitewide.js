$('#create').submit(function() {
	var urllink = $("#linkInput").val();
	console.log(urllink);
	
	$.ajax({
		data: urllink,
		type: $(this).attr('method'),
		url: $(this).attr('action'),
		success: function(data, response) {
			// $('#created').html(data);
			console.log(data);
			console.log(response);
		}
	});
	return false;
});

console.log("hello asdf");