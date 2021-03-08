
$("#email_form").submit(function(e){
	e.preventDefault()
	var user_id = $(this).attr("user_id")
	$.ajax({
		url:`/contact/${user_id}`,
		method: "POST",
		data: $(this).serialize(),
		success: function(response){
			console.log(response)
			// $('#confirm_message').append("<p>Email sent successfully</p>");
			alert("Your email has been sent.");
		}
	})
})

