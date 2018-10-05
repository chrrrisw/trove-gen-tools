// https://stackoverflow.com/questions/1391278/contenteditable-change-events

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

	$("tbody").on("focus", 'td[contenteditable="true"]', function(event) {

		// Copy current content to check for changes.
		const $this = $(this);
		$this.data('before', $this.html());

		// event.preventDefault();
		// console.log(this);


	}).on('keyup paste input', 'td[contenteditable="true"]', function(event) {

		// Change appearance of cell on change.
		const $this = $(this);
		if ($this.data('before') !== $this.html()) {
			$this.addClass("uncommitted");
		}

	}).on('blur', 'td[contenteditable="true"]', function(event) {

		// If the data has changed, send to server
		const $this = $(this);
		if ($this.data('before') !== $this.html()) {
			$this.removeClass("uncommitted");
			$this.data('before', $this.html());
			// $this.trigger('change');
			let person_id = this.parentNode.id;
			socket.send($this.data('type') + " " + person_id + " " + $this.html());
			// socket.send("assessed " + person_id + " " + this.checked);
		}

	});
}
