window.onload = function() {
	console.log("Initialising dropdown");
	$('.ui.search.person.dropdown')
		.dropdown({
			clearable: true,
			allowAdditions: true,
			keys: {
				delimiter: 13
			},
		});
}
