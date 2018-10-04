// https://stackoverflow.com/questions/1391278/contenteditable-change-events

window.onload = function() {
	$("tbody").on("focus", 'td[contenteditable="true"]', function(event) {
		const $this = $(this);
		$this.data('before', $this.html());
		// event.preventDefault();
		// console.log(this);

		// let person_id = this.parentNode.id;
		// socket.send("assessed " + person_id + " " + this.checked);
	}).on('keyup paste input', 'td[contenteditable="true"]', function(event) {
		const $this = $(this);
		if ($this.data('before') !== $this.html()) {
			$this.addClass("uncommitted");
		}
	}).on('blur', 'td[contenteditable="true"]', function(event) {
		const $this = $(this);
		$this.removeClass("uncommitted");
		if ($this.data('before') !== $this.html()) {
			$this.data('before', $this.html());
			// $this.trigger('change');
			let person_id = this.parentNode.id;
			console.log(person_id);
		}
	});
}
