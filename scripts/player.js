// player.js

// Récupérer le paramètre de l'URL pour obtenir le lien de la vidéo
const urlParams = new URLSearchParams(window.location.search);
const videoLink = urlParams.get('link'); // Récupérer le lien de la vidéo

// Définir la source de la vidéo si le lien existe
if (videoLink) {
    const videoPlayer = document.getElementById('video-player');
    videoPlayer.src = videoLink; // Mettre à jour la source de l'iframe
}
