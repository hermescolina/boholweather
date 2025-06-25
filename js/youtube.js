document.addEventListener('DOMContentLoaded', () => {
    const player = document.getElementById('youtubePlayer');
    const input = document.getElementById('videoInput');
    const button = document.getElementById('loadBtn');

    if (!player || !input || !button) return;

    button.addEventListener('click', () => {
        const value = input.value.trim();
        if (!value) {
            alert('Please enter a YouTube URL or ID');
            return;
        }
        const id = extractVideoId(value);
        if (!id) {
            alert('Invalid YouTube URL or ID');
            return;
        }
        player.src = `https://www.youtube.com/embed/${id}`;
    });
});

function extractVideoId(text) {
    const regex = /(?:v=|\/)([\w-]{11})(?:[?&]|$)/;
    const shortRegex = /^[\w-]{11}$/;

    if (shortRegex.test(text)) {
        return text;
    }
    const match = text.match(regex);
    return match ? match[1] : null;
}
