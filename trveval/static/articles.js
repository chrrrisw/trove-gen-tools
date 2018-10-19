window.onload = function() {

	const socket = start_comms();

	console.log("checkboxes");

	// Delegated event for assessed checkboxes
	$("tbody").on("change", "input.assessed", function(event) {
		event.preventDefault();
		// event.stopPropagation();
		let article_id = this.parentNode.parentNode.id;
		socket.send("assessed " + article_id + " " + this.checked);
	});

	// Delegated event for relevant checkboxes
	$("tbody").on("change", "input.relevant", function(event) {
		event.preventDefault();
		// event.stopPropagation();
		let article_id = this.parentNode.parentNode.id;
		socket.send("relevant " + article_id + " " + this.checked);
	});

	// Initialise sidebar
	// TODO Make delegated event.
	// $(".ui.bottom.sidebar")
	// 	.sidebar('setting', 'transition', 'overlay')
	// 	.sidebar('attach events', '.ellipsis.horizontal.icon')
	// ;

}
