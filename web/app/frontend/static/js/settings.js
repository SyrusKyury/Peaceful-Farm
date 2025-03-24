function update_page_content() {}

function sendSettings() {
	const formData = {};
	document.querySelectorAll('#settings-form input, #settings-form textarea').forEach(element => {
		formData[element.name] = element.type === 'checkbox' ? element.checked ? 'true' : 'false' : element.value;
	});

	console.log(JSON.stringify(formData));

	loadingTimeout = setTimeout(() => {
		document.getElementById('loading-screen').classList.remove('hidden');
	}, 2000);

	fetch('/settings', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(formData)
	})
	.then(response => window.location.href = response.url)
	.catch(error => console.error('Error:', error))
	.finally(() => document.getElementById("loading-screen").classList.add("hidden"));
}
