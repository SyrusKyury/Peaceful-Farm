const notification_sound = new Audio('/static/snd/notification.mp3');

function showNotification(message, color) {
	// Create a new notification element
	const notification = document.createElement('div');
	if (color === "green") {
		notification.classList.add('bg-[#54c168]', 'text-white', 'p-4', 'rounded-lg', 'shadow-lg', 'flex', 'items-center', 'justify-between', 'space-x-2');
	} else if (color === "blue") {
		notification.classList.add('bg-[#6ec5e9]', 'text-white', 'p-4', 'rounded-lg', 'shadow-lg', 'flex', 'items-center', 'justify-between', 'space-x-2');
		// Update content
		update_page_content();
	}
	// Play the notification sound
	notification_sound.play();
	// Create the message content with HTML formatting
	const messageElement = document.createElement('div');
	messageElement.innerHTML = message; // Insert HTML content to format the message

	// Create the close button
	const closeButton = document.createElement('button');
	closeButton.classList.add('text-white', 'font-bold');
	closeButton.innerHTML = '&times;';
	closeButton.onclick = function() {
		notification.remove();
	};

	// Add the message and close button to the notification
	notification.appendChild(messageElement);
	notification.appendChild(closeButton);

	// Add the notification to the container
	const container = document.getElementById('notifications-container');
	container.appendChild(notification);

	// Automatically hide the notification after 5 seconds
	setTimeout(() => {
		notification.remove(); // Remove the notification after 5 seconds
	}, 10000);
}


// Ascolta le notifiche dal server (Socket.IO)
const socket = io.connect(g_address);
socket.on('message', function(message) {
	console.log(message);
	showNotification(message.data, message.color || "green");
});

function calculateTickPercentage(startDate, tickDuration) {
	// Get the current date and time
	const currentDate = new Date();

	// Calculate the time difference in milliseconds between the current date and the start date
	const timeDifference = currentDate - new Date(startDate);

	// Calculate the position within the tick (between 0 and tickDuration)
	const tickPosition = timeDifference % tickDuration;

	// Calculate the percentage of the tick completed
	const percentage = (tickPosition / tickDuration) * 100;

	return percentage;
}

function updateProgressBar() {
	const competitionStartDate = g_start; // Start date of the competition (ISO format)
	const tickDuration = g_tick; // Duration of each tick in milliseconds (e.g., 60,000 ms = 1 minute)

	// Calculate the current progress percentage
	const tickPercentage = calculateTickPercentage(competitionStartDate, tickDuration);

	// Update the progress bar width based on the calculated percentage
	const progressBar = document.getElementById('progress-bar');
	progressBar.style.width = `${tickPercentage}%`;
}

document.getElementById('submit-flag-btn').addEventListener('click', function(event) {
	event.preventDefault(); // Evita la navigazione predefinita
	document.getElementById('flag-popup').classList.remove('hidden');
});

document.getElementById('close-popup').addEventListener('click', function() {
	document.getElementById('flag-popup').classList.add('hidden');
});

document.getElementById('submit-flag').addEventListener('click', function() {
	const flag = {
		'Front-End Submission': [document.getElementById('flag-input').value]
	};
	const isUrgent = document.getElementById('urgent-flag').checked;
	const exploit = 'Front-End Submission';
	const service = 'Front-End Submission';
	const nickname = 'Front-End Submission';

	if (document.getElementById('flag-input').value.trim() === "") {

		return;
	}

	fetch('/flags/frontend', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			flags: flag,
			exploit: exploit,
			service: service,
			nickname: nickname,
			urgent: isUrgent
		})
	}).catch(error => {
		// Handle error
		alert('An error occurred. Please try again later.');
		console.log(error);
	});
});

document.getElementById('flag-popup').addEventListener('click', function(event) {
	// Se l'utente clicca sullo sfondo (non sulla finestra del popup)
	if (event.target === this) {
		this.classList.add('hidden');
	}
});


// Update the progress bar every 200 milliseconds
setInterval(updateProgressBar, 10);