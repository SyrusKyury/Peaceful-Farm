function updateTable() {
	fetch('/info_data' + window.location.search)
		.then(response => response.json())
		.then(response => {
			// Sort by the second column (index 1) in descending order
			response.sort((a, b) => new Date(b[1]) - new Date(a[1]));

			const tbody = document.querySelector("table tbody");
			tbody.innerHTML = "";

			response.forEach((row, index) => {
				let trClass = index % 2 === 0 ? "bg-[#eaf9fb]" : "bg-white";

				let tr = document.createElement("tr");
				tr.className = trClass;

				row.forEach(cellData => {
					let td = document.createElement("td");
					td.className = "px-4 py-2 border-b text-[#55a5c0]";
					td.textContent = cellData;
					tr.appendChild(td);
				});

				tbody.appendChild(tr);
			});
		})
		.catch(error => console.error("Error loading data:", error));
}


function update_page_content() {
	updateTable();
}

updateTable();