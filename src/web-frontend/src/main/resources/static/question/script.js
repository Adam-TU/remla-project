$(document).ready(function() {

	function getQuestion() {
		return $("textarea").val().trim()
	}
	
	function cleanResult() {
		$("#result").removeClass("correct")
		$("#result").removeClass("incorrect")
		$("#result").removeClass("error")
		$("#result").html()
	}

	$("button").click(function (e) {
		e.stopPropagation()
		e.preventDefault()

		var question = getQuestion()
		
		$.ajax({
			type: "POST",
			url: "./",
			data: JSON.stringify({"title": question}),
			contentType: "application/json",
			dataType: "json",
			success: handleResult,
			error: handleError	
		})
	})

	function handleResult(res) {
		var tags = res.tags

        if(tags.length === 0) {
            tags = "No tags predicted"
        } else {
            tags = tags.join(", ")
        }

		cleanResult()
		// $("#result").addClass(wasRight ? "correct" : "incorrect")
		$("#result").html("Predicted tags: " + tags)
		$("#result").show()
	}
	
	function handleError(e) {
		cleanResult()		
		$("#result").addClass("error")
		$("#result").html("An error occured (see log).")
		$("#result").show()
	}
	
	$("textarea").on('keypress',function(e) {
		$("#result").hide()
	})
	
	$("input").click(function(e) {
		$("#result").hide()
	})
})