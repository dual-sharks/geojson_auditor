// Handles all event listeners
document.addEventListener('DOMContentLoaded', function() {
    setupMap();
    setupFormSubmission();
});

document.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') {
        console.log('Left arrow key pressed');
        document.getElementById('invalid-button').click();
    } else if (event.key === 'ArrowRight') {
        console.log('Right arrow key pressed');
        document.getElementById('valid-button').click();
    }
});
