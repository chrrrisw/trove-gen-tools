if (!window.indexedDB) {
    window.alert("Your browser doesn't support a stable version of IndexedDB. Please upgrade your browser.");
}

var db;

// Let us open our database

request.onsuccess = function(event) {
  // Do something with request.result!
  db = event.target.result;
};

db.onerror = function(event) {
  // Generic error handler for all errors targeted at this database's
  // requests!
  alert("Database error: " + event.target.errorCode);
};

// This event is only implemented in recent browsers
request.onupgradeneeded = function(event) {
  // Save the IDBDatabase interface
  var db = event.target.result;

  // Create an objectStore for this database
  var objectStore = db.createObjectStore("name", { keyPath: "myKey" });
};


window.onload = function() {
	// var DBOpenRequest = window.indexedDB.open("ArticleDatabase", 1);

	// DBOpenRequest.onerror = function(event) {
	// 	note.innerHTML += '<li>Error loading database.</li>';
	// };

	// DBOpenRequest.onsuccess = function(event) {
	// 	note.innerHTML += '<li>Database initialised.</li>';

	// 	// store the result of opening the database in the db variable. This is used a lot below
	// 	db = DBOpenRequest.result;

	// 	// Run the displayData() function to populate the task list with all the to-do list data already in the IDB
	// 	displayData();
	// };

}
