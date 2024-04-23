document.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') {
        // Left arrow key pressed, mark as invalid
        document.getElementById('invalid-button').click();
    } else if (event.key === 'ArrowRight') {
        // Right arrow key pressed, mark as valid
        document.getElementById('valid-button').click();
    }
});
window.addEventListener('resize', function () {
    map.invalidateSize();
});