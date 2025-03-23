const ctx = document.getElementById('chart').getContext('2d');
let chart;

// Function to handle button click
function handleButtonClick(button) {
	if (button.classList.contains('bg-[#55a5c0]'))
		return

	// Memorize the clicked button into the session storage
	sessionStorage.setItem('clickedButton', button.id);

	// Reset all buttons to default state
	document.querySelectorAll('.flex-row button').forEach(btn => {
		btn.classList.remove('bg-[#55a5c0]');
		btn.classList.add('bg-[#6ec5e9]');
	});

	// Set the clicked button to "pressed" state
	button.classList.remove('bg-[#6ec5e9]');
	button.classList.add('bg-[#55a5c0]');

	const buttonId = button.id.replace('-button', '');
	updateTable(buttonId);
	plot(buttonId);
}


function update_page_content() {
    document.querySelectorAll('.flex-row button').forEach(btn => {
		if (btn.classList.contains('bg-[#55a5c0]')) {
			updateTable(btn.id.replace('-button', ''));
			plot(btn.id.replace('-button', ''));
		}
	});
}


function updateTable(filterGroup) {
	fetch('/group?group=' + filterGroup)
		.then(response => response.json())
		.then(response => {
			const tbody = document.querySelector("table tbody");
			tbody.innerHTML = "";

			// Update the first column name with the filterGroup
			let firstColumnHeader = document.querySelector("table thead th:first-child");
			firstColumnHeader.innerHTML = `
			        <img src="/static/${filterGroup}.png" class="inline-block w-4 h-4 ml-2">
			        ${filterGroup.charAt(0).toUpperCase() + filterGroup.slice(1)}
			        `;


			response.forEach((row, index) => {
				let trClass = index % 2 === 0 ? "bg-[#eaf9fb]" : "bg-white";

				let tr = document.createElement("tr");
				tr.className = trClass;

				row.forEach((cellData, index) => {
					let td = document.createElement("td");
					td.className = "px-4 py-2 border-b text-[#55a5c0]";

					if (index === 0) {
						let a = document.createElement("a");
						a.href = "/info?type=" + filterGroup + "&value=" + cellData;
						a.textContent = cellData;
						a.className = "text-[#54c168] underline hover:text-[#078030] underline";
						td.appendChild(a);
					} else {
						td.textContent = cellData;
					}

					tr.appendChild(td);
				});


				tbody.appendChild(tr);
			});
		})
		.catch(error => console.error("Error loading data:", error));
}


function getRandomColor() {
	return `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`;
}


function plot(group) {
	fetch('/stats?group=' + group)
		.then(response => response.json())
		.then(data => {
			// Estrai tutti gli IP
			const entries = Object.values(data).flatMap(tick => Object.keys(tick));
			const uniqueEntries = [...new Set(entries)];

			// Inizializza il nuovo dizionario
			const result = uniqueEntries.reduce((acc, entry) => {
				acc[`${entry} accepted`] = [];
				acc[`${entry} rejected`] = [];
				return acc;
			}, {});

			// Ordina i tick per chiave (timestamp)
			const sortedTicks = Object.keys(data).sort();

			// Itera in ordine sui tick e aggiorna il dizionario result
			sortedTicks.forEach(tick => {
				const tickData = data[tick];

				uniqueEntries.forEach(entry => {
					const accepted = tickData[entry]?.accepted || 0;
					const rejected = tickData[entry]?.rejected || 0;

					result[`${entry} accepted`].push(accepted);
					result[`${entry} rejected`].push(rejected);
				});
			});

			const datasets = Object.keys(result).map(key => {
				const color = getRandomColor();
				return {
					label: key,
					data: result[key],
					borderColor: color,
					backgroundColor: color.replace(", 1)", ", 0.2)"),
					borderWidth: 2,
					tension: 0.3
				};
			});

			// 7. Creare il grafico con Chart.js
			if (chart) {
				chart.destroy();
			}

			const chartCanvas = document.getElementById('chart');
			chartCanvas.width = 600; // Larghezza fissa
			chartCanvas.height = 100; // Altezza fissa

			chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: sortedTicks, // Asse X con i tick
					datasets: datasets
				},
				options: {
					responsive: true,
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});


		})
		.catch(error => console.error('Errore durante il fetch:', error));
}

document.getElementById('search').addEventListener('input', function() {
	const searchValue = this.value.toLowerCase();
	const rows = document.querySelectorAll("table tbody tr");

	rows.forEach(row => {
		const firstColumnText = row.querySelector("td:first-child")?.textContent.toLowerCase() || "";
		row.style.display = firstColumnText.includes(searchValue) ? "" : "none";
	});
});

// Check session storage for a previously clicked button
const clickedButton = sessionStorage.getItem('clickedButton') || 'ip-button';
document.getElementById(clickedButton).click();