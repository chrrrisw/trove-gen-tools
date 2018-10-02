window.onload = function() {

	console.log("Creating websocket");
	const wsurl = "ws://" + document.location.host + "/ws";
	const socket = new WebSocket(wsurl);

	// Connection opened
	socket.onopen = function(ev) {
		console.log("Opened");
		socket.send('Hello Server!');
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


}