window.onload = function() {

	console.log("Creating websocket");
	const wsurl = "ws://" + document.location.host + "/ws";
	const socket = new WebSocket(wsurl);

	// Connection opened
	socket.onopen = function(ev) {
		console.log("Opened");
	};

	// Listen for messages
	socket.onmessage = function(ev) {
		console.log('Message from server ', ev.data);
	};

	socket.onerror = function(ev) {
		console.log("Error");
	}

	socket.onclose = function(ev) {
		console.log("Closed");
	}

	console.log("chekboxes");

	// Delegated event for assessed checkboxes
	$("tbody").on("change", "input.assessed", function(event) {
		event.preventDefault();
		let article_id = this.parentNode.parentNode.id;
		socket.send("assessed " + article_id + " " + this.checked);
	});

	// Delegated event for relevant checkboxes
	$("tbody").on("change", "input.relevant", function(event) {
		event.preventDefault();
		let article_id = this.parentNode.parentNode.id;
		socket.send("relevant " + article_id + " " + this.checked);
	});

}
