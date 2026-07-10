function updateDateTime() {
    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    document.getElementById('current-datetime').textContent = '🕒 ' + now.toLocaleDateString('en-US', options);
}
updateDateTime();
setInterval(updateDateTime, 60000);