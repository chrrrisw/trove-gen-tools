function start_comms() {

	console.log("Creating websocket");
	const wsurl = "ws://" + document.location.host + "/ws";
	const socket = new WebSocket(wsurl);
	const lightbulb = $(".lightbulb.icon");

	// Connection opened
	socket.onopen = function(ev) {
		console.log("Opened");
		lightbulb.removeClass("red").addClass("green");
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
		lightbulb.removeClass("green").addClass("red");
	}

	return socket;
}
