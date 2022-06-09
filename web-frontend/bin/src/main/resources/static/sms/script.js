$(document).ready(function() {

	function getQuestion() {
		return $("textarea").val().trim()
	}
	
	function getGuess() {
		return $("input[name='guess']:checked").val().trim()
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
		var guess = getGuess()
		
		$.ajax({
			type: "POST",
			url: "./",
			data: JSON.stringify({"question": question, "guess": guess}),
			contentType: "application/json",
			dataType: "json",
			success: handleResult,
			error: handleError	
		})
	})

	function handleResult(res) {
		var wasRight = res.result == getGuess()

		cleanResult()		
		$("#result").addClass(wasRight ? "correct" : "incorrect")
		$("#result").html("The classifier " + (wasRight ? "agrees" : "disagrees"))		
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